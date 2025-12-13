# DSCI 551 Final Project - Darren Parry

import os
import streamlit as st
from parser import SimpleJSONParser
from functions import (filter, projection, group_by, join, aggregate_max, aggregate_sum, aggregate_avg, aggregate_count, aggregate_min)

@st.cache_data
def load_data(file_path):
    # Reads a file from disk, parses it with parser.py and returns the list of businesses in a format that we can use functions.py
    try:
        with open(file_path, 'r') as f:
            json_string = f.read()
        
        # Our custom parser
        parser = SimpleJSONParser()
        data = parser.parse(json_string)
        
        # The list of restaurants is inside the "businesses" key
        if 'businesses' in data:
            return data['businesses']
        else:
            return data
            
    except FileNotFoundError:
        st.error(f"ERROR: File not found at {file_path}")
        return None
    except Exception as e:
        st.error(f"ERROR: Could not parse {file_path}. Reason: {e}")
        return None

@st.cache_data
def load_all_data(directory):
    # Loads and parses all JSON files in a given directory and returns a dictionary mapping filenames to parsed data.
    all_data = {}
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                data = load_data(file_path)
                all_data[filename] = data
    except FileNotFoundError:
        st.error(f"ERROR: Directory not found at {directory}")
        return {}
    except Exception as e:
        st.error(f"ERROR: Could not load data from {directory}. Reason: {e}")
    return all_data

# Start of front-end code for streamlit
st.title("⚾ MLB Restaurant Finder 🌭🍔🍕🌮")
st.write("This web app uses a custom-built JSON parser and NoSQL-like functions to project certain outputs. The MLB restaurant dataset has the following fields that you can sort through: 'id', 'alias', 'name', 'image_url', 'is_closed', 'url', 'review_count', 'categories', 'rating', 'coordinates', 'transactions', 'price', 'location', 'phone', 'display_phone', 'distance'")

data_folder = "data"
all_team_data = load_all_data(data_folder)

# Operation pages
st.sidebar.title("Select Function")

# Helper function to delete the unncecessary information in the .json files
def clean_team_name(team_keys):
    return team_keys\
        .replace('_', ' ') \
        .replace('restaurants', '') \
        .replace(' copy', '') \
        .replace('.json', '') \
        .strip()  

team_keys = list(all_team_data.keys()) 

# Decides which function we want to run showing up as an option on the side of the screen
if not team_keys:
    st.error("No data files found in the data directory.")
else: 
    operation = st.sidebar.radio(
        "Choose a function:",
        ("Filter", "Projection", "Group By & Aggregate", "Join", "Query with Filter, Projection", "Query with Filter, Group, Aggregate", "Query with Filter, Group, Aggregate, Project")
    )

    if operation == "Filter":
        # Chooses which team you want to run the functions on
        st.sidebar.title("Select Team")
        selected_team_key = st.sidebar.selectbox(
        "Choose a team:",
        team_keys,
        format_func=clean_team_name
        )
        data_to_use = all_team_data[selected_team_key]

        st.header(f"Filter data for: {clean_team_name(selected_team_key)}")

        field = st.text_input("Field to filter on (e.g., rating, name, price, location)", "rating")
        op = st.selectbox("Operator", (">=", ">", "==", "<", "<="))
        value = st.text_input("Value to compare (e.g., 4.0)", "4.0")
        try:
            value = float(value)
        except ValueError:
            pass 

        # Runs our filter function
        if st.button("Run Filter"):
            results = filter(data_to_use, field, op, value)
            st.success(f"Found {len(results)} results.")
            st.write(results)

    elif operation == "Projection":
        # Chooses which team you want to run the functions on
        st.sidebar.title("Select Team")
        selected_team_key = st.sidebar.selectbox(
            "Choose a team:", 
            team_keys,
            format_func=clean_team_name
        )
        data_to_use = all_team_data[selected_team_key]
        
        st.header(f"Project data for: {clean_team_name(selected_team_key)}")

        # Gets the list of all of the keys and puts them in a dropdown menu
        if data_to_use:
            sample_record = data_to_use[0]
            all_available_fields = list(sample_record.keys())
            default_cols = [col for col in ["name", "rating", "price"] if col in all_available_fields]
            
            fields_list = st.multiselect(
                "Choose fields to display:", 
                options=all_available_fields,
                default=default_cols
            )

            # Runs our projection function
            if st.button("Run Projection"):
                if not fields_list:
                    st.error("Please select at least one field.")
                else:
                    results = projection(data_to_use, fields_list)
                    st.success(f"Showing {len(results)} records.")
                    st.write(results) 
        else:
            st.warning("This dataset appears to be empty.")

    elif operation == "Group By & Aggregate":
        # Chooses which team you want to run the functions on
        st.sidebar.title("Select Team")
        selected_team_key = st.sidebar.selectbox(
        "Choose a team:",
        team_keys,
        format_func=clean_team_name
        )
        data_to_use = all_team_data[selected_team_key]
        
        st.header(f"Group/Aggregate data for: {clean_team_name(selected_team_key)}")
        
        group_field = st.text_input("Field to group by (e.g., price, id, rating)", "price")
        agg_field = st.text_input("Field to aggregate (e.g., rating, review_count, transactions)", "rating")
        agg_func = st.selectbox("Function", ("max", "avg", "count", "sum", "min"))
        
        # Runs our group by & aggreagtion function
        if st.button("Run Aggregation"):
            grouped_data = group_by(data_to_use, group_field)
            results = []
            for group_name, documents in grouped_data.items():
                if agg_func == 'max':
                    agg_value = aggregate_max(documents, agg_field)
                elif agg_func == 'avg':
                    agg_value = aggregate_avg(documents, agg_field)
                elif agg_func == 'count':
                    agg_value = aggregate_count(documents)
                elif agg_func == 'sum':
                    agg_value = aggregate_sum(documents, agg_field)
                elif agg_func == 'min':
                    agg_value = aggregate_min(documents, agg_field)
                else:
                    agg_value = "Function not implemented"
                
                results.append({
                    group_field: group_name,
                    f"{agg_func}_{agg_field}": agg_value
                })
            
            st.write(results)

    elif operation == "Join":
        st.header("Join Data")
        st.write("Find matching restaurants between two teams.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Chooses the first team you want to run the join function on
            selected_team1_key = st.selectbox(
            "Choose Team 1:",
            team_keys, 
            format_func=clean_team_name  
            )
            key1 = st.text_input("Join Key for Team 1 (e.g., name)", "name")
            data1 = all_team_data[selected_team1_key]
            
        with col2:
            # Chooses the second team you want to run the join function on
            selected_team2_key = st.selectbox(
            "Choose Team 2:",
            team_keys, 
            format_func=clean_team_name
            )
            key2 = st.text_input("Join Key for Team 2 (e.g., name)", "name")
            data2 = all_team_data[selected_team2_key]
        
        # Runs our join function
        if st.button("Run Join"):
            if data1 is None or data2 is None:
                st.error("One or both datasets could not be loaded.")
            else:
                results = join(data1, key1, data2, key2)
                st.success(f"Found {len(results)} matching restaurants.")
                st.write(results)

    elif operation == "Query with Filter, Projection":
        # Chooses which team you want to run the functions on
        selected_team_key = st.sidebar.selectbox(
        "Choose a team:",
        team_keys,
        format_func=clean_team_name
        )
        data_to_use = all_team_data[selected_team_key]
        st.header(f"Querying: **{clean_team_name(selected_team_key)}**")

        if data_to_use:
            # Uses our filter function first
            st.subheader("First, filter the data:")
            filter_field = st.text_input("Filter field (e.g., rating, name, price, location)", "rating")
            filter_op = st.selectbox("Operator", (">=", ">", "==", "<", "<="))
            filter_value = st.text_input("Value (e.g., 4.5)", "4.5")
            
            # Then, we use our project function
            st.subheader("Second, project the results:")
            # Uses the same function we used earlier to get a dropdown of all of the options
            sample_record = data_to_use[0]
            all_available_fields = list(sample_record.keys())
            default_cols = [col for col in ["name", "rating", "price"] if col in all_available_fields]
            fields_list = st.multiselect(
                "Choose fields to display:", 
                options=all_available_fields,
                default=default_cols
            )
            
            # Uses both functions to run the query
            if st.button("Run Query"):
                try:
                    try:
                        filter_value = float(filter_value)
                    except ValueError:
                        pass

                    # First runs our filter function
                    filtered_results = filter(data_to_use, filter_field, filter_op, filter_value)
                    
                    # Then, runs our projection function
                    final_results = projection(filtered_results, fields_list)
                    
                    st.success(f"Found {len(final_results)} final results.")
                    st.write(final_results)
                
                except Exception as e:
                    st.error(f"An error occurred during the query: {e}")

    elif operation == "Query with Filter, Group, Aggregate":
        # Chooses which team you want to run the functions on
        selected_team_key = st.sidebar.selectbox(
        "Choose a team:",
        team_keys,
        format_func=clean_team_name
        )
        data_to_use = all_team_data[selected_team_key]
        st.header(f"Querying: **{clean_team_name(selected_team_key)}**")

        if data_to_use:
            # First, we get our filter inputs for our filter function
            st.subheader("First, filter the data:")
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_field = st.text_input("Filter field (e.g., rating, name, price)", "rating")
            with col2:
                filter_op = st.selectbox("Operator", (">=", ">", "==", "<", "<=", "!="))
            with col3:
                filter_value = st.text_input("Value (e.g., 4.0)", "4.0")
            
            st.markdown("---")

            # Second, we get our group by & aggregate inputs for our group by & aggregate function
            st.subheader("Second, group & aggregate the filtered results:")
            col4, col5, col6 = st.columns(3)
            with col4:
                group_field = st.text_input("Group by (e.g., price, id, rating)", "price")
            with col5:
                agg_field = st.text_input("Aggregate field (e.g., rating, transactions)", "rating")
            with col6:
                agg_func = st.selectbox("Function", ("count", "max", "min", "avg", "sum"))
            
            # Run the query using our two functions 
            if st.button("Run Query"):
                try:
                    try:
                        filter_value = float(filter_value)
                    except ValueError:
                        pass 

                    # Run our filter function
                    filtered_results = filter(data_to_use, filter_field, filter_op, filter_value)
                    st.info(f"Step 1 (Filter) kept {len(filtered_results)} records.")

                    if not filtered_results:
                        st.warning("Filter removed all data. Cannot group.")
                    else:
                        # Run our group by function
                        grouped_data = group_by(filtered_results, group_field)
                        
                        # Run our aggregate function
                        final_results = []
                        for group_name, documents in grouped_data.items():
                            if agg_func == 'max':
                                val = aggregate_max(documents, agg_field)
                            elif agg_func == 'min':
                                val = aggregate_min(documents, agg_field)
                            elif agg_func == 'avg':
                                val = aggregate_avg(documents, agg_field)
                            elif agg_func == 'sum':
                                val = aggregate_sum(documents, agg_field)
                            elif agg_func == 'count':
                                val = aggregate_count(documents)
                            else:
                                val = "Error"

                            final_results.append({
                                group_field: group_name,
                                f"{agg_func}_{agg_field}": val
                            })
                        
                        # Display final results
                        st.success("Chain Completed Successfully!")
                        st.write(final_results)
                
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    elif operation == "Query with Filter, Group, Aggregate, Project":
        # Chooses which team you want to run the functions on
        selected_team_key = st.sidebar.selectbox(
        "Choose a team:",
        team_keys,
        format_func=clean_team_name
        )
        data_to_use = all_team_data[selected_team_key]
        st.header(f"Querying: **{clean_team_name(selected_team_key)}**")        
        if data_to_use:
            # Get our filter inputs for our filter function
            st.subheader("First, filter the data:")
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_field = st.text_input("Filter field (e.g., rating, name, price)", "rating")
            with col2:
                filter_op = st.selectbox("Operator", (">=", ">", "==", "<", "<=", "!="))
            with col3:
                filter_value = st.text_input("Value (e.g., 3.5)", "3.5")
            
            st.markdown("---") 

            # Get our group by inputs for our group by function
            st.subheader("Second, group the filtered data:")
            group_field = st.text_input("Group by field (e.g., price, id, rating)", "price")
            agg_target_field = st.text_input("Field to calculate stats on (e.g., rating, transactions)", "rating")

            st.markdown("---") 

            # Get our projection inputs for our projection inputs
            st.subheader("Third, project the grouped and filtered data:")
            options = [group_field, 'Count', f'Max_{agg_target_field}', f'Avg_{agg_target_field}']
            selected_columns = st.multiselect("Choose columns to display:", options, default=options)
            
            # Run query wiht our three functions
            if st.button("Run Query"):
                try:
                    try:
                        filter_value = float(filter_value)
                    except ValueError:
                        pass 

                    # Use our filter function
                    filtered_results = filter(data_to_use, filter_field, filter_op, filter_value)
                    
                    if not filtered_results:
                        st.warning("Filter removed all data. Stopping.")
                    else:
                        st.info(f"Filter kept {len(filtered_results)} records.")

                        # Use our group by function
                        grouped_data = group_by(filtered_results, group_field)
                        
                        # Use our aggreagtion function
                        aggregated_results = []
                        for group_name, documents in grouped_data.items():
                            
                            count_val = aggregate_count(documents)
                            max_val = aggregate_max(documents, agg_target_field)
                            avg_val = aggregate_avg(documents, agg_target_field)
                            
                            summary_doc = {
                                group_field: group_name,
                                'Count': count_val,
                                f'Max_{agg_target_field}': max_val,
                                f'Avg_{agg_target_field}': avg_val
                            }
                            aggregated_results.append(summary_doc)

                        # Use our projection function
                        final_output = projection(aggregated_results, selected_columns)
                        
                        st.success("Pipeline Complete!")
                        st.write(final_output)
                
                except Exception as e:
                    st.error(f"An error occurred: {e}")