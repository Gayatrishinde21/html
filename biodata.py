from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import psycopg2

HOST = "localhost"
PORT = 8000

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            with open("biodata.html", "r", encoding="utf-8") as file:
                html = file.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/save_data":
            # Parse form data including file upload
            content_type = self.headers.get('Content-Type')
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Expected multipart/form-data")
                return

            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                             'CONTENT_TYPE': content_type})

            fname = form.getvalue("fname")
            lname = form.getvalue("lname")
            address = form.getvalue("address")
            dob = form.getvalue("date")
            phone = form.getvalue("phone")
            email = form.getvalue("email")
            gender = form.getvalue("gender")

            # Handle multiple hobbies
            hobbies_list = form.getlist("hobbies")
            hobbies = ",".join(hobbies_list)

            # Handle photo upload
            photo_file = form["photo"]
            photo_filename = ""
            if photo_file.filename:
                photo_filename = os.path.basename(photo_file.filename)
                os.makedirs("photos", exist_ok=True)
                with open(f"photos/{photo_filename}", "wb") as f:
                    f.write(photo_file.file.read())

            try:
                conn = psycopg2.connect(
                    dbname="my_db",
                    user="postgres",
                    password="root",
                    host="localhost",
                    port="5432"
                )
                cur = conn.cursor()
                query = f"""
                    INSERT INTO biodata (fname, lname, address, dob, phone, email, gender, hobbies, photo)
                    VALUES ('{fname}', '{lname}', '{address}', '{dob}', '{phone}', '{email}', '{gender}', '{hobbies}', '{photo_filename}')
                """
                cur.execute(query)
                conn.commit()
                cur.close()
                conn.close()

                self.send_response(200)
                self.end_headers()
                self.wfile.write("Data saved successfully.".encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error saving data: {str(e)}".encode())

def run():
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Server running on http://{HOST}:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run()
