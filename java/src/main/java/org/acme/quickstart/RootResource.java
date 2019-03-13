package org.acme.quickstart;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Optional;
import java.util.Properties;

@Path("/account")
public class RootResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String root() throws ClassNotFoundException, SQLException {
        StringBuilder accounts = new StringBuilder();
        // Load the Postgres JDBC driver.
        Class.forName("org.postgresql.Driver");

        // Connect to the "bank" database.
        Properties props = new Properties();
        props.setProperty("user", get_env("DB_USER", "maxroach"));
        props.setProperty("sslmode", "disable");
        try (Connection db = DriverManager
                .getConnection(String.format("jdbc:postgresql://%s:%s/%s",
                        get_env("DB_URL", "localhost"),
                        get_env("DB_PORT", "26257"),
                        get_env("DB_TABLE", "bank")), props)) {
            // Create the "accounts" table if not exists
            db.createStatement()
                    .execute("CREATE TABLE IF NOT EXISTS accounts (id INT PRIMARY KEY, balance INT)");

            // Print out the balances.
            ResultSet res = db.createStatement()
                    .executeQuery("SELECT id, balance FROM accounts");
            while (res.next()) {
                accounts.append(String.format("\taccount %s: %s\n",
                        res.getInt("id"),
                        res.getInt("balance")));
            }
        }
        if (accounts.toString().length() == 0) return "No Accounts Found";
        return accounts.toString();
    }

    private String get_env(String env_var, String default_value) {
        return Optional.ofNullable(System.getenv(env_var)).orElse(default_value);
    }
}