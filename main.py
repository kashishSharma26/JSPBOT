from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from db_conn import local  # Assuming this imports the necessary database connection details

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)


# Function to handle database connection
def fun():
    try:
        f1 = mysql.connector.connect(  # Assuming mysql.connector is imported and defined elsewhere
            host=host,
            user=user,
            password=password,
            database=database
        )
        if f1.is_connected():
            print("success")
            f1.commit()
            return f1
    except NameError:
        return "DENIED"


# Define Flask resource for API endpoint
class API(Resource):
    def post(self):
        output = request.get_json()
        query = output['query'].lower()
        email = str(output['email'])
        match query:
            case "applications":
                l1 = local()
                l1.is_connected()
                mycursor = l1.cursor()
                sql1 = "select application_id , application_name from application_list"
                mycursor.execute(sql1)
                record1 = mycursor.fetchall()
                sql3 = "select application_id from application_list"
                mycursor.execute(sql3)
                return record1
            case _:
                if query <= str(query.startswith('')):
                    print(query)
                    l1 = local()
                    mycursor = l1.cursor()
                    sql3 = "select application_id from application_list"
                    mycursor.execute(sql3)
                    record5 = mycursor.fetchall()
                    record5 = str(record5)
                    if query in record5:
                        l1 = local()
                        mycursor = l1.cursor()
                        sql2 = "select title , fkey from function_list where application_id = %s "
                        mycursor.execute(sql2, [query])
                        record2 = mycursor.fetchall()
                        if query <= str(query.startswith('')):
                            l1 = local()
                            sql = "select password from application_list where application_id = %s "
                            mycursor = l1.cursor()
                            mycursor.execute(sql, [query])
                            result = mycursor.fetchall()
                            global password
                            password = str(result)[3:-4]
                            print(password)
                            sql1 = "select server_ip from application_list where application_id = %s "
                            mycursor = l1.cursor()
                            mycursor.execute(sql1, [query])
                            result = mycursor.fetchall()
                            global host
                            host = str(result)[3:-4]
                            print(host)
                            sql = "select user from application_list where application_id = %s "
                            mycursor = l1.cursor()
                            mycursor.execute(sql, [query])
                            result = mycursor.fetchall()
                            global user
                            user = str(result)[3:-4]
                            print(user)
                            sql = "select database_name from application_list where application_id = %s "
                            mycursor = l1.cursor()
                            mycursor.execute(sql, [query])
                            result = mycursor.fetchall()
                            global database
                            database = str(result)[3:-4]
                            print(database)
                            fun()
                            # Send message to Google Chat
                            room_id = output['room_id']
                            message = "Your response message here"
                            send_message_to_google_chat(room_id, message)
                            return jsonify(record2, "ENTER FUNCTION ID")
                        else:
                            return jsonify("NO ID FOUND")
                    elif query.startswith(''):
                        q1 = str(query).upper()
                        l1 = local()
                        mycursor = l1.cursor()
                        sql3 = "select fkey from function_list"
                        mycursor.execute(sql3)
                        record3 = str(mycursor.fetchall())
                        if q1 in record3:
                            fx = fun()
                            print(fx)
                            if fx == "DENIED":
                                return jsonify("PLEASE TYPE RESPECTIVE APPLICATION_ID")
                            else:
                                sql4 = "select query from function_list where fkey = %s"
                                mycursor.execute(sql4, [query])
                                record4 = str(mycursor.fetchall())
                                result1 = (record4.replace('flag', email))
                                result2 = result1[3: -4]
                                mycursor_1 = fx.cursor()
                                mycursor_1.execute(result2)
                                record5 = mycursor_1.fetchall()
                                # Send message to Google Chat
                                room_id = output['room_id']
                                message = "Your response message here"
                                send_message_to_google_chat(room_id, message)
                                return jsonify(record5)
                        else:
                            return jsonify("Type Correct Function id")

        # Return response
        return jsonify("Response sent to Google Chat")


# Add resource to API with endpoint
api.add_resource(API, '/api/sendRequest')

# Run Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
