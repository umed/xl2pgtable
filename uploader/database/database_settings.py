class DatabaseSettings:
    user = "postgres"
    password = "pswd"
    database = "postgres"
    host = "127.0.0.1"
    schema = "public"

    def __iter__(self):
        yield "database", self.database
        yield "host", self.host
        yield "user", self.user
        yield "password", self.password
