define(['./es'], function(ElasticSearch) {
    'use strict';

    describe('elastic query builder', function() {

        beforeEach(module(function($provide) {
            $provide.service('es', ElasticSearch);
        }));

        it('generates query string query for q param', inject(function(es) {
            var body = es({q: 'test'});
            expect(body.query.query_string.query).toBe('test');
            expect(body.from).toBe(0);
            expect(body.size).toBe(25);
        }));

        it('generates match all query for empty q param', inject(function(es) {
            var body = es({});
            expect(body.query.match_all).toEqual({});
        }));

        it('generates filtered query when using filter', inject(function(es) {
            var filters = [
                {term: {type: 'picture'}},
                {term: {provider: 'foo'}}
            ];

            var body = es({}, filters);
            expect(body.query.filtered.query.match_all).toEqual({});
            expect(body.query.filtered.filter.and.length).toBe(2);
        }));

        it('does pagination', inject(function(es) {
            var body = es({page: 2});
            expect(body.from).toBe(25);
        }));
    });
});
