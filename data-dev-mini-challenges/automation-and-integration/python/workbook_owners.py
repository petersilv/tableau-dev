# ----------------------------------------------------------------------------
from credentials import tableau as creds
from sign_in import sign_in

import requests
import json
import pandas

import tableauhyperapi as hyp


# ----------------------------------------------------------------------------
def workbooks():

    auth = sign_in()

    url = f"{creds.server}/api/3.7/sites/{auth['credentials']['site']['id']}/workbooks"

    headers = {'content-type': 'application/json',
               'accept': 'application/json',
               'X-tableau-auth': auth['credentials']['token']}

    response = requests.get(url, headers=headers)

    workbook_dict = json.loads(response.text)

    return workbook_dict['workbooks']['workbook']


# ----------------------------------------------------------------------------
def workbook_owners():

    workbook_list = workbooks()
    
    workbook_owners_dict = [{'workbook_name': w['name'], 'owner': w['owner']['name']} 
                            for w 
                            in workbook_list]

    return workbook_owners_dict


# ----------------------------------------------------------------------------
def workbook_owners_to_csv(path='../data/workbook_owners.csv'):

    workbook_owners_dict = workbook_owners()

    pandas.DataFrame.from_dict(workbook_owners_dict) \
                    .to_csv(path, index=False, encoding='utf-8')

    print(f'Workbook Owners file successfully created at: {path}\n')


# ----------------------------------------------------------------------------
def workbook_owners_publish():

    workbook_owners_dict = workbook_owners()

    with hyp.HyperProcess(hyp.Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        print("The HyperProcess has started.")

        with hyp.Connection(hyper.endpoint, '../data/workbook_owners.hyper', hyp.CreateMode.CREATE_AND_REPLACE) as connection:
            print("The connection to the Hyper file is open.")

            connection.catalog.create_schema('Extract')

            table = hyp.TableDefinition(hyp.TableName('Extract','Extract'), 
                                            [
                                                hyp.TableDefinition.Column('workbook_name', hyp.SqlType.text()),
                                                hyp.TableDefinition.Column('owner',         hyp.SqlType.text())
                                            ])

            print("The table is defined.")

            connection.catalog.create_table(table)

            with hyp.Inserter(connection, table) as inserter:

                for i in workbook_owners_dict:

                    inserter.add_row( [ i['workbook_name'], i['owner'] ] )

                inserter.execute()

            print("The data was added to the table.")
        print("The connection to the Hyper extract file is closed.")
    print("The HyperProcess has shut down.")


# ----------------------------------------------------------------------------

if __name__ == "__main__":
    workbook_owners_to_csv()

