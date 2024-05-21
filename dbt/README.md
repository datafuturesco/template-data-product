## Configure DBT

You can place any DBT files in here. You will need to alter a few files to ensure the default values match your needs.

### dbt_project.yml

##### `name` argument

You will need to alter the `<PROJECT_NAME>` value with your project name. Please note, `-`'s and `spaces` will not work. Please use underscores.

##### `models` argument

This will also have to be modified under the `models:` argument as the first referenced point is the profile name.

##### `+database` argument

Lastly, you will want to change the `+database:` key to match your project.

### profiles.yml

This file defines the defaults for all variables. Replace all the `UPDATE ME` with proper corresponding values related to Snowflake.
And modify `<DBT_PROFILE>` with your snowflake profile created.
