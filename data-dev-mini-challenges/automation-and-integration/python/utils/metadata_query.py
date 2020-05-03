query = """
{
  workbooks {
    projectName
    name
    owner {
      email
      name
    }
    embeddedDatasources {
      name
      fields{
      	  ... on CalculatedField {
          name
        } 
      }
    }
  }
}
"""