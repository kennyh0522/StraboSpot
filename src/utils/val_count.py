#use this to see value counts of each column. The builtin value_counts function in the pandas libary is hard to read, so with val_count, it makes it a bit easier

def val_count(data):
    counter = 0
    for i in data.columns:
        
        # if i in ["properties_viewed_timestamp" ,"properties_modified_timestamp","properties_symbology_circleColor","properties_id","properties_symbology_lineColor","properties_symbology_lineWidth","properties_symbology_lineDasharray","properties_sed_strat_section_strat_section_id","properties_strat_section_id","properties_symbology_fillColor","properties_orientation_id","properties_custom_fields_osm_id","properties_orientation_modified_timestamp","properties_custom_fields_id","properties_orientation_unix_timestamp","properties_gps_accuracy","properties_altitude","properties_notesTimestamp"]: 
        
        print(counter)
        print(data[i].value_counts())
        counter += 1
        print("=========================="*5)
    print(data.shape)