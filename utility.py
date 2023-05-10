def get_fips(state):
    # Pull FIPS value
    with open("./data/fips.txt") as fips_file:
        for line in fips_file:
            state_fip = line.strip().split(maxsplit=1)
            if state_fip[1] == state.upper():
                fips_code = state_fip[0]
                return(fips_code)
            else:
                continue 

def prep_call():
    from gql.transport.aiohttp import AIOHTTPTransport
    from gql import Client
    import os

    #Hasura headers
    HASURA_URL = os.environ.get('HASURA_URL')
    HASURA_HEADERS = {"X-Hasura-Admin-Secret": os.environ.get('HASURA_ADMIN_SECRET')}

    transport = AIOHTTPTransport(url=HASURA_URL, headers=HASURA_HEADERS)

    client = Client(transport=transport, fetch_schema_from_transport=True)

    return(client)

def assert_model(payload,model='BaseMetric'):
    from metadata_schema.MetricSchema import BaseMetric,ClientMetricExt,ServiceMetricExt

    if model == 'BaseMetric':
        BaseMetric(**payload)
        metric_send(payload)
    elif model == 'ClientMetricExt':
        ClientMetricExt(**payload)
    elif model == 'ServiceMetricExt':
        ServiceMetricExt(**payload)
    else:
        return

def state_send(payload):
    from gql import Client, gql

    client = prep_call()

    query = gql(
    """
    mutation insert_state {
    insert_state(objects: {fips: "%s", year: %s, url: "%s", state_name: "%s"}) {
        returning {
        fips
        year
        url
        state_name
        }
    }
    }

    """ % (payload['fips_code'],int(payload['year']), payload['url'], payload['state'].title())
    )

    result = client.execute(query)

def prep_base_payload(payload):
    from gql import gql

    query = gql(
    """
    mutation insert_base_metrics {
    insert_metrics(objects: {state_name: "%s", year: %s, domain: "%s", table_name: "%s", metric_name: "%s", metric_result: %s}) {
        returning {
        state_name
        year
        domain
        table_name
        metric_name
        metric_result
        }
    }
    }

    """ % (payload['state_name']
           ,int(payload['year'])
            , payload['domain']
            , payload['table_name']
            , payload['metric_name']
            ,payload['metric_result'])
    )

    return(query)

def metric_send(payload):
    from time import sleep

    client = prep_call()

    query = prep_base_payload(payload)

    result = client.execute(query)

    sleep(1)