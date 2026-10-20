/* Generate importable, public-only documentation without changing runtime APIs. */
const fs = require('node:fs');
const path = require('node:path');
const converter = require('swagger2openapi');
const SwaggerParser = require('@apidevtools/swagger-parser');

const DOC_DIR = __dirname;
const HTTP_METHODS = new Set(['get', 'post', 'put', 'patch', 'delete', 'head', 'options']);

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(DOC_DIR, name), 'utf8'));
}

function writeJson(name, value) {
  fs.writeFileSync(path.join(DOC_DIR, name), JSON.stringify(value, null, 2) + '\n');
}

function publicSwagger(swagger, routes) {
  const result = structuredClone(swagger);
  const paths = {};
  // Import only endpoints already visible on the public site. A new annotation
  // alone must not publish an internal or experimental endpoint.
  for (const identity of Object.keys(routes.endpoints)) {
    const [method, route] = identity.split(' ');
    const operation = result.paths[route]?.[method.toLowerCase()];
    if (!operation) throw new Error(`Published endpoint missing from Swagger: ${identity}`);
    paths[route] ??= {};
    paths[route][method.toLowerCase()] = operation;
  }
  result.paths = paths;
  return result;
}

async function buildSpecification(swagger, environments, examples, routes) {
  const converted = await converter.convertObj(publicSwagger(swagger, routes), {targetVersion: '3.0.3'});
  const spec = converted.openapi;
  spec.servers = environments.environments.map(environment => ({
    url: environment.baseUrl,
    description: environment.name,
  }));
  for (const example of examples.examples) {
    const operation = spec.paths[example.path]?.[example.method];
    if (!operation) throw new Error(`Example references an unpublished endpoint: ${example.path}`);
    const media = operation.requestBody?.content?.['application/json'];
    if (!media) throw new Error(`Example has no JSON request body: ${example.path}`);
    media.examples ??= {};
    if (media.examples[example.name]) throw new Error(`Duplicate request example: ${example.path} ${example.name}`);
    media.examples[example.name] = {
      summary: example.summary,
      description: example.description,
      value: example.request,
    };
    delete media.example;

    const status = String(example.http_status);
    operation.responses[status] ??= {
      description: 'Observed parameter validation response.',
      content: {'application/json': {schema: {$ref: '#/components/schemas/internal_server_http.J'}}},
    };
    const response = operation.responses[status].content?.['application/json'];
    if (!response) throw new Error(`Example has no JSON response: ${example.path} ${status}`);
    response.examples ??= {};
    response.examples[example.name] = {
      summary: example.summary,
      description: `Captured from ${examples.network} on ${examples.captured_on}; values may change.`,
      value: example.response,
    };
    delete response.example;
  }
  // Validation dereferences its input, so validate a copy and retain the compact
  // internal references in the published artifact. Never resolve external URLs.
  await SwaggerParser.validate(structuredClone(spec), {resolve: {external: false}});
  return spec;
}

function schemaText(value, schemas, seen = new Set()) {
  if (!value || typeof value !== 'object') return '';
  const chunks = [];
  if (value.$ref?.startsWith('#/components/schemas/')) {
    const name = value.$ref.slice('#/components/schemas/'.length);
    if (!seen.has(name)) {
      seen.add(name);
      chunks.push(schemaText(schemas[name], schemas, seen));
    }
  }
  if (value.description) chunks.push(value.description);
  for (const [name, property] of Object.entries(value.properties ?? {})) {
    chunks.push(name, schemaText(property, schemas, seen));
  }
  for (const item of value.allOf ?? []) chunks.push(schemaText(item, schemas, seen));
  if (value.items) chunks.push(schemaText(value.items, schemas, seen));
  return chunks.join(' ');
}

function buildSearchIndex(spec, nativeDocs, routes) {
  const entries = [];
  const schemas = spec.components.schemas;
  for (const [route, methods] of Object.entries(spec.paths)) {
    for (const [method, operation] of Object.entries(methods)) {
      if (!HTTP_METHODS.has(method)) continue;
      const identity = `${method.toUpperCase()} ${route}`;
      const url = routes.endpoints[identity];
      if (!url) throw new Error(`No public documentation URL for ${identity}`);
      entries.push({
        title: operation.summary,
        url,
        category: operation.tags?.[0] ?? 'API',
        description: operation.description ?? '',
        text: [identity, JSON.stringify(operation['x-synonyms'] ?? []),
          schemaText(operation.requestBody?.content?.['application/json']?.schema, schemas),
          ...Object.values(operation.responses).map(response =>
            schemaText(response.content?.['application/json']?.schema, schemas))].join(' '),
      });
    }
  }
  function addDocuments(group) {
    for (const item of group.items ?? []) {
      if (!item.content) continue;
      const name = item.type === 'folder' ? group.name : item.name;
      const url = routes.documents[name];
      if (!url) throw new Error(`No public documentation URL for ${name}`);
      entries.push({title: item.name, url, category: 'Guides', description: '', text: item.content});
    }
    for (const child of group.children ?? []) addDocuments(child);
  }
  for (const group of nativeDocs.docCollection) addDocuments(group);
  return {entries};
}

async function generate() {
  const routes = readJson('public-routes.json');
  const spec = await buildSpecification(readJson('swagger.json'), readJson('environments.json'),
    readJson('examples.json'), routes);
  writeJson('apidog.openapi.json', spec);
  writeJson('search-index.json', buildSearchIndex(spec, readJson('subscan.apidog.json'), routes));
  console.log(`Generated public OpenAPI (${Object.keys(routes.endpoints).length} endpoints) and full-text search index.`);
}

module.exports = {publicSwagger, buildSpecification, buildSearchIndex};
if (require.main === module) {
  generate().catch(error => { console.error(error.message); process.exitCode = 1; });
}
