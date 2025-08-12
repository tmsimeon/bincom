#!/bin/bash

# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo service postgresql start

# Switch to postgres user and set password
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'bincom';"

echo "PostgreSQL installed and password for 'postgres' user set to 'bincom'."
echo "You can now connect using: psql -U postgres -h localhost -W"


# make the file executable && run the script
# chmod +x install_postgres.sh
# ./install_postgres.sh