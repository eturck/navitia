from v1 import Index
from v1 import Uri
from v1 import Coverage
from v1 import Journeys
from v1 import Schedules
from v1 import Places
from v1 import converters_collection_type
def v1_routing(api):
    api.add_resource(Index.Index,
                     '/v1/',
                     endpoint='v1.index')

    collections = converters_collection_type.collections_to_resource_type.keys()
    str_collections = ", ".join(collections)
    coverage = '/v1/coverage/'
    region = coverage + '<string:region>/'
    coord = coverage + '<float:lon>;<float:lat>/'
    collection_id = '<any('+str_collections+'):collection>/<string:id>'

    api.add_resource(Coverage.Coverage,
                     coverage[:-1],
                     coverage,
                     region[:-1],
                     region,
                     coord[:-1],
                     coord,
                     endpoint='v1.coverage')

    api.add_resource(Uri.Collection,
                    region + '<any('+str_collections+'):collection>',
                    region + '<any('+str_collections+'):collection>/',
                    coord + '<any('+str_collections+'):collection>',
                    coord + '<any('+str_collections+'):collection>/',
                    region + '<path:uri>/<any('+str_collections+'):collection>',
                    region + '<path:uri>/<any('+str_collections+'):collection>/',
                    coord + '<path:uri>/<any('+str_collections+'):collection>',
                    coord + '<path:uri>/<any('+str_collections+'):collection>/',
                    endpoint = 'v1.collection')


    api.add_resource(Places.Places,
                     region+'places',
                     coord+'places',
                     region+'places/',
                     coord+'places/',
                     endpoint = 'v1.places'
                     )

    api.add_resource(Places.PlacesNearby,
                     region+'places_nearby',
                     coord+'places_nearby',
                     region+'places_nearby/',
                     coord+'places_nearby/',
                     region+'<path:uri>/places_nearby',
                     coord+'<path:uri>/places_nearby',
                     endpoint = 'v1.places_nearby'
                     )

    api.app.add_url_rule('/v1/coverage/'+collection_id, 'v1.uriredirect',
                         Uri.Redirect)
    api.add_resource(Uri.Uri,
                    region + collection_id,
                    region + '<path:uri>/'+collection_id,
                    coord + collection_id,
                    coord + '<path:uri>/' + collection_id,
                    region + collection_id+'/',
                    region + '<path:uri>/'+collection_id+'/',
                    coord + collection_id+'/',
                    coord + '<path:uri>/' + collection_id+'/',
                    endpoint='v1.uri')

    api.add_resource(Journeys.Journeys,
                     region + '<path:uri>/journeys',
                     coord + '<path:uri>/journeys',
                     '/v1/journeys',
                     endpoint='v1.journeys'
                     )

    api.add_resource(Schedules.RouteSchedules,
                     region + '<path:uri>/route_schedules',
                     coord + '<path:uri>/route_schedules',
                     '/v1/route_schedules',
                     endpoint='v1.route_schedules'
                     )

    api.add_resource(Schedules.NextArrivals,
                     region + '<path:uri>/arrivals',
                     coord + '<path:uri>/arrivals',
                     '/v1/arrivals',
                     endpoint='v1.arrivals'
                     )

    api.add_resource(Schedules.NextDepartures,
                     region + '<path:uri>/departures',
                     coord + '<path:uri>/departures',
                     '/v1/departures',
                     endpoint='v1.departures'
                     )
    api.add_resource(Schedules.StopSchedules,
                     region + '<path:uri>/stop_schedules',
                     coord + '<path:uri>/stop_schedules',
                     '/v1/stop_schedules',
                     endpoint='v1.stop_schedules',
                     )
