const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const {publicSwagger, buildSpecification, buildSearchIndex} = require('./generate-openapi.cjs');

const read = name => JSON.parse(fs.readFileSync(path.join(__dirname, name), 'utf8'));

test('publication allowlist preserves public operations without exposing newly annotated endpoints', () => {
  const swagger = {paths: {'/public': {get: {summary: 'Visible'}}, '/internal': {post: {summary: 'Internal'}}}};
  const routes = {endpoints: {'GET /public': '/api-1'}};
  assert.deepEqual(Object.keys(publicSwagger(swagger, routes).paths), ['/public']);
  assert.ok(swagger.paths['/internal']);
  assert.throws(() => publicSwagger(swagger, {endpoints: {'GET /missing': '/api-2'}}), /missing from Swagger/);
});

test('generated OpenAPI is reproducible, validates and retains reader-supplied authentication', async () => {
  const spec = await buildSpecification(read('swagger.json'), read('environments.json'),
    read('examples.json'), read('public-routes.json'));
  assert.deepEqual(spec, read('apidog.openapi.json'));
  assert.deepEqual(spec.security, [{ApiKeyAuth: []}]);
  assert.equal(spec.components.securitySchemes.ApiKeyAuth.name, 'X-API-Key');
  assert.equal(spec.components.securitySchemes.ApiKeyAuth.in, 'header');
  assert.equal(spec.components.securitySchemes.ApiKeyAuth.default, undefined);
  assert.equal(spec.servers[0].url, 'https://polkadot.api.subscan.io');
  assert.equal(spec.servers.length, 60);
  const actual = Object.entries(spec.paths).flatMap(([route, methods]) =>
    Object.keys(methods).map(method => `${method.toUpperCase()} ${route}`)).sort();
  assert.deepEqual(actual, Object.keys(read('public-routes.json').endpoints).sort());
});

test('named examples preserve minimal requests and observed HTTP validation errors', () => {
  const spec = read('apidog.openapi.json');
  const transfer = spec.paths['/api/v2/scan/transfers'].post;
  const examples = transfer.requestBody.content['application/json'].examples;
  assert.deepEqual(examples.latest.value, {row: 2, page: 0});
  assert.ok(examples.account.value.address);
  assert.ok(examples.block_range.value.block_range);
  assert.equal(transfer.responses['400'].content['application/json'].examples.invalid_page_size.value.code, 400);
  for (const item of read('examples.json').examples) {
    assert.ok(spec.paths[item.path][item.method].requestBody.content['application/json'].examples[item.name]);
    assert.ok(spec.paths[item.path][item.method].responses[item.http_status]);
  }
});

test('examples cannot add an unpublished operation or silently overwrite another scenario', async () => {
  const routes = read('public-routes.json');
  const examples = read('examples.json');
  examples.examples.push({...examples.examples[0]});
  await assert.rejects(buildSpecification(read('swagger.json'), read('environments.json'), examples, routes), /Duplicate request example/);
  examples.examples = [{...examples.examples[0], path: '/internal-only'}];
  await assert.rejects(buildSpecification(read('swagger.json'), read('environments.json'), examples, routes), /unpublished endpoint/);
});

test('full-text index covers public links, field names and guide body content', () => {
  const index = buildSearchIndex(read('apidog.openapi.json'), read('subscan.apidog.json'), read('public-routes.json'));
  assert.deepEqual(index, read('search-index.json'));
  assert.ok(index.entries.find(entry => entry.title === 'Tutorial').text.includes('X-API-Key'));
  assert.ok(index.entries.find(entry => entry.title === 'List transfers').text.includes('after_id'));
  assert.ok(index.entries.every(entry => /^\/(api|doc|folder)-\d+$/.test(entry.url)));
  const urls = index.entries.map(entry => entry.url);
  assert.equal(new Set(urls).size, urls.length);
});
