import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import json
import psycopg2
import psutil
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.set_page_config(page_title="Metric Reporting")
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """

st.markdown(hide_default_format, unsafe_allow_html=True)

# Connect to the database
conn = psycopg2.connect(database="dbms", user="testuser", password="test", host="localhost", port="5432")

# Create a cursor object
cur = conn.cursor()


# https://towardsdatascience.com/how-to-use-streamlits-st-write-function-to-improve-your-streamlit-dashboard-1586333eb24d

st.title("Metric Reporting")
# im = Image.open('/analyse.png')
# st.set_page_config(page_title="Metric Reporting", page_icon = im)
st.header("An Interface to know the Query Processing Metrics!")
st.subheader("Get Table Statistics, Memory usage in runtime and much more ...")
st.image('https://assets.toptal.io/images?url=https://bs-uploads.toptal.io/blackfish-uploads/components/blog_post_page/content/cover_image_file/cover_image/1272403/retina_500x200_0712-Bad_Practices_in_Database_Design_-_Are_You_Making_These_Mistakes_Dan_Newsletter-f90d29e5d2384eab9f4f76a0a18fa9a8.png')
# Try to insert bg image


query = st.text_input("Enter the SQL Query")
if(st.button('Analyse')):
       # Execute the query with EXPLAIN ANALYZE
       cur.execute("BEGIN;")
       start_cpu = psutil.cpu_percent(interval=1)
       start_mem = psutil.virtual_memory().used
       temp = "EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON) " + query
       print(temp)
       cur.execute(temp)
       end_mem = psutil.virtual_memory().used
       end_cpu = psutil.cpu_percent(interval=1)
       # cpu_usage = (start_cpu + end_cpu) / 2
       cpu_usage = end_cpu
       process = psutil.Process()
       memory_info = process.memory_info()

       # Fetch all rows of the output
       rows = cur.fetchall()
       cur.execute("ROLLBACK;")

       # Concatenate the rows into a single string
       output = ""
       for row in rows[0][0]:
              # output += json.dumps(row)
              # print(row['Plan'])
              print(row)
              del row['Plan']['Output']
              # print(row['Plan'])
              df = pd.DataFrame.from_dict(row['Plan'], orient='index')
              df.reset_index(inplace=True)
              df.rename(columns = {'index': 'Parameter', 0: 'Value'}, inplace = True)
              print(df)
              # print_dict(row, 0)
              # print('*******')
              qid=row['Query Identifier']
              plan_time=row['Planning Time']
              exe_time=row['Execution Time']
              # print('////')
              actual_rows=row['Plan']['Actual Rows']
              width=row['Plan']['Plan Width']
       
       throughput= (actual_rows*width*1000)/(exe_time*1024*1024)
       print("CPU Usage : ",cpu_usage, "%")
       print("Query Identifier:", qid)
       print("Execution Time:", exe_time, "ms")
       print("Planning Time:", plan_time, "ms")
       print("Memory Usage (RSS):", memory_info.rss, "bytes")
       print("Memory Usage (VMS):", memory_info.vms, "bytes")
       print("Throughput : ",throughput,"MBps" )

       col1, col2 = st.columns(2)
       with col1:
              st.subheader("Successfully analysed")
              st.success(query)
              st.subheader("Common Metrics")
              st.text("Query Identifier: {}".format(qid))
              st.code("CPU Usage: {} %".format(cpu_usage))
              st.code("Execution Time: {} ms".format(exe_time))
              st.code("Planning Time: {} ms".format(plan_time))
              st.code("Memory Usage (RSS): {} MB".format(memory_info.rss/(1024*1024)))
              st.code("Memory Usage (VMS): {} MB".format(memory_info.vms/(1024*1024)))
              st.code("Throughput: {} MBps".format(throughput))
       with col2:
              st.subheader("Plan Table Metrics")
              AgGrid(df, fit_columns_on_grid_load=True)


