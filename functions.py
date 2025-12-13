# DSCI 551 Final Project - Darren Parry

def filter(data, field, operator, value):
    # Function that takes an empty result and filters the list into the given operator
    results = []
    for document in data:
        if field not in document:
            continue
        if field in document:
            doc_value = document[field]
            if operator == '==':
                if doc_value == value:
                    results.append(document)
            elif operator == '!=':
                if doc_value != value:
                    results.append(document)
            elif operator == '<':
                if doc_value < value:
                    results.append(document)
            elif operator == '<=':
                if doc_value <= value:
                    results.append(document)
            elif operator == '>':
                if doc_value > value:
                    results.append(document)
            elif operator == '>=':
                if doc_value >= value:
                    results.append(document)
    return results

def projection(data, fields):
    # Function that takes an empty list and projects only said data
    results = []
    for document in data:
        projected_doc = {field: document[field] for field in fields if field in document}
        results.append(projected_doc)
    return results

def group_by(data, field):
    # Function that groups like data with data fields
    grouped_data = {}
    for document in data:
        key = document.get(field)
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(document)
    return grouped_data

def aggregate_sum(data, field):
    # Function that adds up the given field
    total = 0
    for document in data:
        if field in document and isinstance(document[field], (int, float)):
            total += document[field]
    return total

def aggregate_avg(data, field):
    # Function that averages out the given field
    total = 0
    count = 0
    for document in data:
        if field in document and isinstance(document[field], (int, float)):
            total += document[field]
            count += 1
    return total / count if count > 0 else 0

def aggregate_count(data):
    # Function that counts the amount of data
    return len(data)

def aggregate_max(data, field):
    # Function that gets the max of the given data field
    max_value = None
    for document in data:
        if field in document and isinstance(document[field], (int, float)):
            if max_value is None or document[field] > max_value:
                max_value = document[field]
    return max_value

def aggregate_min(data, field):
    # Function that gets the min of the given data field
    min_value = None
    for document in data:
        if field in document and isinstance(document[field], (int, float)):
            if min_value is None or document[field] < min_value:
                min_value = document[field]
    return min_value

def join(data1, data1_key, data2, data2_key):
    # Function that performs a nested loop join and handles key collisions by renaming keys from the second dataset.
    results = []
    for doc1 in data1:
        for doc2 in data2:
            if data1_key in doc1 and data2_key in doc2 and doc1[data1_key] == doc2[data2_key]:
                merged_doc = doc1.copy()
                for key, value in doc2.items():                    
                    if key == data2_key:
                        continue                        
                    if key in merged_doc:
                        merged_doc[f"{key}_2"] = value
                    else:
                        merged_doc[key] = value
                        
                results.append(merged_doc)  
    return results