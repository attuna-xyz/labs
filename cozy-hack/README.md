
# GitHub Bot for Prompt-Engineered Code Generation

This project uses the Julep API to create an AI agent that generates high-quality cookbooks and tutorials for open-source software projects. It then automatically creates a pull request with the generated content on GitHub.

## Features

- Creates an AI agent using the Julep API
- Loads and processes documents from specified URLs
- Generates Python code based on a given task
- Automatically creates a pull request on GitHub with the generated code

## Prerequisites

- Python 3.7+
- Julep API key
- GitHub repository with proper permissions
- Existing seed set of cookbooks or tutorials

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install the required packages:
   ```
   pip install julep langchain-community langchain-text-splitters
   ```

3. Set up environment variables:
   ```
   export JULEP_API_KEY=your_julep_api_key
   export JULEP_API_URL=your_julep_api_url
   ```

## Configuration

Edit the `config.py` file to customize:
- Project information
- Document URLs
- Agent configuration
- Task description

## Usage

Run the main script:
```
python main.py
```

This will:
1. Create an AI agent
2. Load and process specified documents
3. Generate a Python script based on the configured task
4. Create a pull request on GitHub with the generated code

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.