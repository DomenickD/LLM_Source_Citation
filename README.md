# Ollama RAG Chatbot

For layman's introduction to tunning this application, click [here](#how-to-run-this-app-on-your-own-computer)

To Run: 
1. Install the required libraries by running `pip install -r requirements.txt` in your terminal.

2. Switch to project directory:
```cd Projectv8```

3. Run the chatbot with:
```streamlit run app.py```

## LLM Demonstration

This section showcases the step-by-step functionality of the LLM through individual screenshots, followed by an animated GIF summarizing the interaction.

<!-- ## Summary GIF -->

<!-- Below is an animated GIF summarizing the demonstration: -->

<!-- ![LLM Demonstration GIF](Pictures/LLM_GIF.gif) -->

## Screenshots

![Screenshot 1](Pictures/llm_1.png)
![Screenshot 2](Pictures/llm_2.png)
![Screenshot 3](Pictures/llm_3.png)
![Screenshot 4](Pictures/llm_4.png)
![Screenshot 5](Pictures/llm_5.png)
![Screenshot 6](Pictures/llm_6.png)
![Screenshot 7](Pictures/llm_7.png)
![Screenshot 8](Pictures/llm_8.png)

## How to this from scratch

Open Command line terminal (Windows key then "cmd". Then "enter" key)

- In the command line, type: `chmod +x start.sh`

- Type `./start.sh`

It will start to download and check system requirments in order to run the app. 

### How to Run This App on Your Own Computer

1. **Install Python (version 3.10 or newer)**  
   - Go to [python.org](https://www.python.org/downloads) and download the latest Python 3.x installer for Windows.  
   - Run the installer. On the first setup screen, make sure to check the box **"Add Python to PATH"** so that your computer can run Python from the Command Prompt.
   - Adding something to the path can be confusing, but if you're on Windows, follow these steps:  
     
     1. Type `env` in the search bar.  
     2. Click on **Edit the system environment variables**.  
     3. Click on **Environment Variables...** at the bottom right.  
     4. In the **System variables** section, find the `Path` variable.  
     5. Click **Edit...**.  
     6. Click **New**.  
     7. Add the path to your Python installation. For example:  
        `C:\\Users\\YourName\\AppData\\Local\\Programs\\Python\\Python310`.  
   - Once installed, you can verify the installation by opening your Command Prompt (type `CMD` in the Windows search bar) and typing:
     ```bash
     python --version
     ```
     It should show a version number like `Python 3.x.x`.

2. **Install a Code Editor (Optional but Recommended: VS Code)**  
   - Go to [code.visualstudio.com](https://code.visualstudio.com) and download **Visual Studio Code**.  
   - Install it using all the default options.  
   - Open VS Code, then use **File → Open Folder** to navigate to a folder where you want to store this project.

3. **Download (or Copy) the App Files**  
   1. Visit the repository in your browser:  
      `https://github.com/DomenickD/LLM_Source_Citation/tree/main`.  
   2. Click **Code** > **Download ZIP**.  
   3. Extract the ZIP to a folder.

4. **Open a Terminal / Command Prompt**  
   - In VS Code, you can open a terminal by going to **View → Terminal**.  
   - Or, open the Windows Command Prompt (`cmd.exe`) and change directories to the folder where the app files are. For example:
     ```bash
     cd C:\\Users\\YourName\\Documents\\my_streamlit_app
     ```

5. **Install Required Python Libraries**  
   - Inside that folder, run the following command to install all needed packages (including Streamlit):
     ```bash
     pip install -r requirements.txt
     ```

6. **Run the App**  
   - After libraries finish installing, start the app by typing:
     ```bash
     streamlit run app.py
     ```
     (Replace `app.py` with the actual name of your main Streamlit file if it's something else like `main.py`.)  
   - This will launch a local server and automatically open your default web browser to show the Streamlit app at an address like:  
     `http://localhost:8501`.

7. **Use the App**  
   - Your app will appear in the browser, just like it does here on Streamlit Cloud.  
   - As long as the terminal window is open and running, the app will be live on your computer.

**That's it!** Now you can modify the code in VS Code, save changes, and when you refresh your browser, you'll see updates in your app.
