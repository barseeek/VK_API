# Comics Publisher

This Python script downloads a random XKCD comic, uploads it to a [VK](https://vk.com) group's wall, and publishes it as a post.

## How to install

1. Clone the repository to your computer:
    ```
    git clone https://github.com/barseeek/VK_API.git
    ```
2. Navigate to the project directory:
    ```
    cd VK_API
    ```
3. Install the necessary dependencies (Python3 should be already installed):
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Create a `.env` file in the project's root directory and add the required environment variables:
    ```
    VK_ACCESS_TOKEN=YOUR_VK_ACCESS_TOKEN
    VK_GROUP_ID=YOUR_VK_GROUP_ID
    ```
2. Run the script to run the website locally:
    ```
    python main.py
    ```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
