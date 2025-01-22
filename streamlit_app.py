import streamlit as st
import psutil
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="NSAI - Process & Workflow Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a sidebar for navigation
st.sidebar.title("NSAI Tools")
selected_page = st.sidebar.radio(
    "Select Tool",
    ["Process Monitor", "Workflow Tracker"]
)

if selected_page == "Process Monitor":
    st.title("Process Monitor")
    st.write("Monitor CPU and memory usage of running processes")

    # CPU Analysis Section
    duration = st.slider("Recording Duration (seconds)", 1, 30, 5)
    
    if st.button("Start Recording"):
        with st.spinner(f"Recording for {duration} seconds..."):
            # Data collection
            process_data = defaultdict(lambda: {'cpu': [], 'memory': []})
            
            # Progress bar
            progress_bar = st.progress(0)
            start_time = time.time()
            
            while (time.time() - start_time) < duration:
                # Update progress
                elapsed = time.time() - start_time
                progress_bar.progress(elapsed / duration)
                
                for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                    try:
                        proc_info = proc.info
                        process_data[proc_info['name']]['cpu'].append(proc_info['cpu_percent'])
                        process_data[proc_info['name']]['memory'].append(proc_info['memory_percent'])
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                time.sleep(0.1)

            # Process the collected data
            results = {}
            for proc_name, data in process_data.items():
                cpu_values = [cpu for cpu in data['cpu'] if cpu is not None]
                memory_values = [mem for mem in data['memory'] if mem is not None]
                
                if cpu_values and memory_values:
                    results[proc_name] = {
                        'avg_cpu_percent': sum(cpu_values) / len(cpu_values),
                        'avg_memory_percent': sum(memory_values) / len(memory_values),
                        'max_cpu_percent': max(cpu_values),
                        'max_memory_percent': max(memory_values)
                    }

            # Create visualizations
            df = pd.DataFrame.from_dict(results, orient='index')
            
            # Display charts side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top CPU Consumers")
                fig_cpu = plt.figure(figsize=(10, 6))
                plt.bar(df.nlargest(10, 'avg_cpu_percent').index, 
                       df.nlargest(10, 'avg_cpu_percent')['avg_cpu_percent'])
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Average CPU Usage (%)')
                st.pyplot(fig_cpu)

            with col2:
                st.subheader("Top Memory Consumers")
                fig_mem = plt.figure(figsize=(10, 6))
                plt.bar(df.nlargest(10, 'avg_memory_percent').index,
                       df.nlargest(10, 'avg_memory_percent')['avg_memory_percent'])
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Average Memory Usage (%)')
                st.pyplot(fig_mem)

            # Display detailed results
            st.subheader("Detailed Process Analysis")
            st.dataframe(df.round(2))

elif selected_page == "Workflow Tracker":
    st.title("Workflow Tracker")
    st.write("Track and analyze workflow patterns")
    
    # Add workflow tracking functionality here
    st.info("Workflow tracking feature is under development")