from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch_dsl import Search
from requests_aws4auth import AWS4Auth
import boto3


if __name__=='__main__':
    print "Start program"

    host = 'vpc-cloudtrail-log-analysis-mw6nxceelz7zgwfhnn6ij7gugq.eu-west-1.es.amazonaws.com'
    awsauth = AWS4Auth('AKIAIG27VKXRWNLOY7XQ', 'G1e2pyUodE0i/lPaWy++xSGyCqeiUsbL03Zqdzb/', 'eu-west-1', 'es')

####################################################################################################### QUI RUN SENZA PROXY
    try:
        client = boto3.client('ec2')

        ######################    DEVI USARE PER FORZA L HOT SPOT SENZA PROXY   -- ricorda di settare le configurazioni di accesso o con variabili d'ambiente oppure con tilde/.aws
        response = client.describe_tags(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        'i-04412e4a5cccf815c',
                    ]
                },
            ],
        )

        for res in response["Tags"]:
            print 'ResourceId: ', res["ResourceId"], " Key: ", res["Key"], " Value: ", res["Value"]



    except Exception as E:
        print "Unable to connect to AWS"
        print E
        exit(3)

###################################################################################################### QUI RUN CON IL PROXY PER GLI STESSI MOTIVI PER CUI NON FUNZIONA LA MIA VPN
    try:
        es = Elasticsearch(
            hosts=[{'host': host, 'port': 80}],
            http_auth=awsauth,
            #use_ssl=True,
            #verify_certs=True,
            connection_class=RequestsHttpConnection
        )

        print(es.cluster.health())

        #le query non funzionano danno read timeout
        #res = es.search(index='test.abc.logstash', q="*", _source=True, request_timeout=300, allow_no_indices=True)
        #print res['_source']

        es.indices.delete(index='temp-test', ignore=[400, 404])

        campo1 = "ciao11111"
        campo2 = "ciao00"
        retval = es.index(index='temp-test', doc_type='temp', body={
            'campo2': campo2,
            'campo1': campo1,
        })

    except Exception as E:
        print "Unable to connect to", host
        print E
        exit(3)



