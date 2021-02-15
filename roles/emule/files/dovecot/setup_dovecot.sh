cat <<EOL >mysql -uroot
CREATE DATABASE IF NOT EXISTS email_accounts;
grant ALL on email_accounts.* to "Admin"@"localhost" identified by "changeme";
FLUSH PRIVILEGES;
EOL
mysql -uAdmin -pchangeme < ./mysql.initial.sql
