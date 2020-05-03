# ----------------------------------------------------------------------------
from credentials import tableau as creds
from utils import send_email, metadata_query

import tableauserverclient as tsc

# ----------------------------------------------------------------------------
def query_metadata_api():

    # Authenticate
    tableau_auth = tsc.TableauAuth(creds.username, creds.password, creds.site)

    # Identify server
    server = tsc.Server(creds.server, use_server_version=3.7)

    # Read query from file
    query = metadata_query.query

    # Sign in to server and query Metadata API
    with server.auth.sign_in(tableau_auth):
        metadata_response = server.metadata.query(query)

    return metadata_response

# ----------------------------------------------------------------------------
def bad_calculations():

    metadata_response = query_metadata_api()

    # Create inital list
    bad_calc_workbooks = []

    # Loop through workbooks on server
    for w in metadata_response['data']['workbooks']:
        bad_calc_count = 0

        # Loop through datasources in workbook
        for d in w['embeddedDatasources']:

            bad_calcs = []

            # Identify fiels that contain 'calculation' or 'test' 
            for f in d['fields']:

                if 'name' in f:
                    field_name = f['name'].lower()

                    if 'calculation' in field_name \
                    or 'test'        in field_name:

                        bad_calcs.append(f)
                        bad_calc_count += 1

            # Replace original field list with bad calculations list
            d['fields'] = bad_calcs
        
        # Include workbook in output if it contains bad calculations
        if bad_calc_count > 0:
            bad_calc_workbooks.append(w)

    return bad_calc_workbooks


# ----------------------------------------------------------------------------
def email_users_with_bad_calculations():

    # Find bad calcs with function
    bad_calc_workbooks = bad_calculations()

    # Get unique list of users to email
    users_to_email = []
                
    for w in bad_calc_workbooks:
        owner = w['owner']['email']
        if owner not in users_to_email: 
            users_to_email.append(owner) 

    # Loop through users in list to email with details about bad calculations
    for u in users_to_email:

        message_body = ''
        message_intro = 'This email is to let you know that you have some workbooks on Tableau Server that contain poorly named calculations, please see below for the details:\n'

        # Loop through workbooks owned by the user
        for w in bad_calc_workbooks:

            if w['owner']['email'] == u:

                for d in w['embeddedDatasources']:

                    fields = ''
                    
                    for f in d['fields']:
                        fields += f"    - [{f['name']}]\n"

                    divider = '-' * 80

                    message_body += f"\n{divider}\n\nProject: {w['projectName']}  |  Workbook: {w['name']}  |  Datasource: {d['name']}\n\n Poorly Named Calculated Fields:\n{fields}\n{divider}"

        # Build full message
        message = message_intro + message_body

        # Send email
        send_email.send(recipient = w['owner']['email'], 
                        subject   = 'Tableau Server Status Report: Poorly Named Calculations', 
                        message   = message)


if __name__ == "__main__":
    email_users_with_bad_calculations()