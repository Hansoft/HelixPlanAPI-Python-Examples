# -*- coding: utf-8 -*-
""" A simple implementation of Helix Plans's API.
"""
import requests


class HansoftGraphQLClient():
    def __init__(self, url, user, password):
        self.url = url
        self.session = requests.Session()
        if not self.login(user, password):
            print("Could not login")
            return

    def login(self, user, password):
        query = """mutation login($loginCredentials:LoginUserInput!){
          login(loginUserInput:$loginCredentials){
            access_token}
        }
        """

        variables = {"loginCredentials": {
            'username': user,
            'password': password}}

        json, errors = self.execute(query, variables)

        if errors:
            return False

        if not json:
            return False

        token = json["login"]["access_token"]

        self.session.headers["Authorization"] = f"Bearer {token}"

        return True

    def execute(self, query, variables=None):

        try:
            r = self.session.post(self.url, json={
                'query': query, 'variables': variables})
            r.raise_for_status()
        except requests.HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
            return None, None
        except Exception as err:
            print(f'Other error occured: {err}')
            return None, None

        json = r.json()
        if "errors" in json:
            print(json["errors"])
            return json["data"], json["errors"]
        else:
            return json["data"], None

    def nameIdDictionary(self, response):
        items = {}
        for i in response:
            items[i["name"]] = i["id"]
        return items

    def nameQAIdDictionary(self, response):
        items = {}
        for i in response:
            items[i["name"]] = i["qa"]["id"]
        return items

    def IdNameDictionary(self, response):
        items = {}
        for i in response:
            items[i["id"]] = i["name"]
        return items

    """
    List
    """

    def listProjects(self):
        query = """query {projects {name id}}"""
        response, errors = self.execute(query)
        projects = self.nameIdDictionary(response["projects"])
        return projects

    def listProjectsQA(self):
        query = """query {projects {name qa {id}}}"""
        response, errors = self.execute(query)
        print(response["projects"])
        projects = self.nameQAIdDictionary(response["projects"])
        return projects

    def listUsers(self):
        query = """query {users {name id}}"""
        response, errors = self.execute(query)
        users = self.nameIdDictionary(response["users"])
        return users

    def listGroups(self):
        query = """query {userGroups {name id}}"""
        response, errors = self.execute(query)
        groups = self.nameIdDictionary(response["userGroups"])
        return groups

    def listItems(self, project_id, find_query=None):
        if not find_query:
            query = """query Items($id:ID!) {items(id:$id) { id name }}"""
            variables = {"id": project_id}
        else:
            query = """query Items($id:ID!, $findQuery:String) {
                  items(id:$id, findQuery:$findQuery) { id name }}"""
            variables = {"id": project_id, "findQuery": find_query}
        response, errors = self.execute(query, variables)
        items = self.IdNameDictionary(response["items"])
        return items

    def listReleases(self, project_id):
        query = """query Items($id:ID!, $findQuery:String) {
              items(id:$id, findQuery:$findQuery) {
                id
                name
                ... on Release {
                  date
                }
            }}"""
        variables = {"id": project_id, "findQuery": "itemtype=Release"}
        response, errors = self.execute(query, variables)
        items = {}
        for i in response["items"]:
            items[i["name"]] = i["date"]
        return items

    def listColumns(self, project_id):
        query = """query Columns($id:ID!) {
              columns(id:$id) {
                name}}"""
        variables = {"id": project_id}
        response, errors = self.execute(query, variables)
        columns = []
        for column in response["columns"]:
            columns.append(column["name"])
        return columns

    """"
    Create
    """

    def createProject(self, name):
        query = """mutation SimpleCreateProjectForDemo(
            $options: CreateProjectInput!)
            {createProject(createProjectInput: $options) { name id }}"""
        variables = {"options": {
            'name': name}}

        response, errors = self.execute(query, variables)
        if errors:
            if errors[0]["message"] == "Project with that name already exists":
                return -1
            else:
                print(errors)
                return 0
        else:
            return response["createProject"]["id"]

    def createNormalUser(self, name):
        query = """mutation createNormalUser(
              $userPropertiesInput: CreateNormalUserInput!)
              { createNormalUser(createNormalUserInput: $userPropertiesInput)
              { name id } }"""

        variables = {"userPropertiesInput": {"name": name,
                                             "password": "hpmadm"}}
        response, errors = self.execute(query, variables)
        if errors:
            if errors[0]["message"] == "User with that name already exists":
                return -1
            else:
                print(errors)
                return 0
        else:
            return response["createNormalUser"]["id"]

    def createUserGroup(self, name):
        query = """mutation createUserGroup(
                $userGroupPropertiesInput: CreateUserGroupInput!)
              { createUserGroup(createUserGroupInput:
                $userGroupPropertiesInput)
              { name id } }"""

        variables = {"userGroupPropertiesInput": {"name": name}}
        response, errors = self.execute(query, variables)

        if errors:
            existing_msg = "User group with that name already exists"
            if errors[0]["message"] == existing_msg:
                return -1
            else:
                print(errors)
                return 0
        else:

            return response["createUserGroup"]["id"]

    def createBug(self, project_qa_id, name):
        query = """mutation createBugs($project: ID!,
                $bugData: [CreateBugInput]!)
                { createBugs(projectID: $project,
                createBugsInput: $bugData) { name }}"""
        variables = {
            "project": project_qa_id,
            "bugData": [{"name": name}]
        }

        response, errors = self.execute(query, variables)
        if errors:

            print(errors)
            return 0
        else:
            return response["createBugs"]

    """
    Update
    """

    def enableLogin(self, user_id):
        query = """mutation updateNormalUser(
              $userPropertiesInput: UpdateNormalUserInput!)
              { updateNormalUser(updateNormalUserInput: $userPropertiesInput)
              { name id } }"""

        variables = {
            "userPropertiesInput": {
                "id": user_id,
                "accessRights": {
                    "isActiveAccount": True,
                    "documentManagement": True,
                    "dashboards": True,
                    "dashboardPageShare": True,
                    "avatarManagement": True
                }
            }
        }
        response, errors = self.execute(query, variables)

        if errors:
            print(errors)
        else:
            return response["updateNormalUser"]["id"]

    def enableAdmin(self, user_id):
        query = """mutation updateNormalUser(
              $userPropertiesInput: UpdateNormalUserInput!)
              { updateNormalUser(updateNormalUserInput: $userPropertiesInput)
              { name id } }"""

        variables = {
            "userPropertiesInput":
                {"id": user_id,
                 "accessRights": {"admin": True,
                                  "portfolioAllocation": True}
                 }
        }

        response, errors = self.execute(query, variables)

        if errors:
            print(errors)
        else:
            return response["updateNormalUser"]["id"]

    def addUserToGroup(self, group_id, user_id):
        query = """mutation updateUserGroup(
              $updateUserGroupInput: UpdateUserGroupInput!)
              { updateUserGroup(updateUserGroupInput: $updateUserGroupInput)
              { name id } }"""

        variables = {"updateUserGroupInput": {"id": group_id,
                                              "userIDs": [user_id]}}
        response, errors = self.execute(query, variables)

        if errors:
            print(errors)
        else:
            return response["updateUserGroup"]["id"]

    def addUsersToGroup(self, group_id, user_list):
        query = """mutation updateUserGroup(
              $updateUserGroupInput: UpdateUserGroupInput!)
              { updateUserGroup(updateUserGroupInput: $updateUserGroupInput)
              { name id } }"""

        variables = {"updateUserGroupInput": {"id": group_id,
                                              "userIDs": user_list}}
        response, errors = self.execute(query, variables)

        if errors:
            print(errors)
        else:
            return response["updateUserGroup"]["id"]

    def addUserToProject(self, project_id, user_id):
        query = """mutation addProjectUser(
              $project:ID!, $usr:ID!)
              { addProjectUser(projectID:$project, userID:$usr)
              { name id } }"""

        variables = {"project": project_id, "usr": user_id}
        response, errors = self.execute(query, variables)

        if errors:
            print(errors)
        else:
            return response["addProjectUser"]["id"]

    def addGroupToProject(self, project_id, group_id):
        query = """mutation addProjectUserGroup(
              $project:ID!, $group:ID!)
              { addProjectUserGroup(projectID:$project, userGroupID:$group)
              { name id } }"""

        variables = {"project": project_id, "group": group_id}
        response, errors = self.execute(query, variables)

        if errors:
            print(errors)
        else:
            return response["addProjectUserGroup"]["id"]

    def enableMainManager(self, project_id, user_id):
        query = """mutation updateProjectUserAccessRights(
              $project:ID!, $user:ID!, $access:ProjectUserAccessRightsInput!)
              { updateProjectUserAccessRights(projectID:$project,
                userID:$user, accessRights:$access)
              { user {id} } }"""

        variables = {"project": project_id, "user": user_id,
                     "access": {"isMainManager": True,
                                "canAccessProjectHistory": True}}
        response, errors = self.execute(query, variables)

        if errors:
            print(errors)
        else:
            return response["updateProjectUserAccessRights"]["user"]["id"]
