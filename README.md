# Enola AI: GenAI Validation and Observability Platform

Enola AI is an advanced GenAI platform designed to validate and monitor the robustness of artificial intelligence models in highly regulated industries such as finance, healthcare, and education. Our solution ensures that AI implementations comply with strict regulatory standards through continuous assessments, seamless integrations, and real-time monitoring.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Initializing Tracking](#initializing-tracking)
    - [Example: Basic Tracking Initialization](#example-basic-tracking-initialization)
    - [Creating and Registering Steps](#creating-and-registering-steps)
    - [Closing Steps](#closing-steps)
    - [Finalizing and Sending Data to the Server](#finalizing-and-sending-data-to-the-server)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Multilevel Evaluation**: Collect feedback from users, automated assessments, and reviews from internal experts.
- **Real-Time Monitoring**: Continuous monitoring capabilities to detect deviations in AI model behavior.
- **Seamless Integration**: Compatible with existing infrastructures such as ERP systems, CRM platforms, and data analytics tools.
- **Customizable Configuration**: Adapt the evaluation methodology according to the specific needs of the client.
- **Security and Compliance**: Advanced security measures and compliance with data protection regulations.

---

## Requirements

- **Python 3.7+**
- **Dependencies**: Specified in `requirements.txt`

---

## Installation

Before installing the Enola AI SDK, ensure that you have Python 3.7 or higher installed.

1. **Install the SDK via pip**

   ```bash
   pip install enola
   ```

2. **Optional: Create a Virtual Environment**

   It's recommended to use a virtual environment to manage your dependencies.

   ```bash
   python3 -m venv enola-env
   source enola-env/bin/activate  # On Windows use `enola-env\Scripts\activate`
   ```

3. **Install Dependencies**

   If you are installing from the source code, install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Getting Started

To start using the Enola AI SDK, follow the steps below to initialize tracking in your application.

### Initializing Tracking

#### **1. Set Up Environment Variables**

You need to set your Enola API token as an environment variable. Replace `'your_api_token'` with your actual token.

On Linux/macOS:

```bash
export ENOLA_TOKEN='your_api_token'
```

On Windows Command Prompt:

```cmd
set ENOLA_TOKEN=your_api_token
```

Alternatively, you can load it from a `.env` file or set it directly in your script (not recommended for production):

```python
token = 'your_api_token'
```

#### **2. Import the Necessary Libraries**

```python
from enola.tracking import Tracking
from enola.enola_types import ErrOrWarnKind, DataType
import os
```

#### **3. Initialize the Tracking Agent**

```python
# Load the token from environment variables
token = os.getenv('ENOLA_TOKEN')

# Initialize the tracking agent
monitor = Tracking(
    token=token,
    name="My Enola Project",  # Name of your tracking session
    is_test=True,             # Set to True if this is a test session
    app_id="my_app_id",       # Application ID
    app_name="My App",        # Application Name
    user_id="user_123",       # User ID
    user_name="John Doe",     # User Name
    session_id="session_456", # Session ID
    session_name="Session 1", # Session Name
    channel_id="web",         # Channel ID (e.g., 'web', 'mobile')
    channel_name="Web App",   # Channel Name
    ip="192.168.1.1",         # IP address of the client
    message_input="Hello, how can I help you today?"  # Input message from the user
)
```

---

#### **Example: Basic Tracking Initialization**

```python
import os
from enola.tracking import Tracking

# Set up your token
token = os.getenv('ENOLA_TOKEN')

# Initialize the tracking agent
monitor = Tracking(
    token=token,
    name="Customer Support Session",
    is_test=False,
    user_id="customer_001",
    user_name="Alice Smith",
    app_id="support_app",
    app_name="Customer Support App",
    channel_id="live_chat",
    channel_name="Live Chat",
    session_id="session_789",
    session_name="Support Session 789",
    message_input="I need help with my order."
)
```

---

### Creating and Registering Steps

A **step** represents a significant stage in your agent's processing workflow. For example, you might create a step for data retrieval and another for model inference.

#### **1. Create a New Step**

```python
# Create a generic step
step1 = monitor.new_step("Data Retrieval Step")
```

#### **2. Add Extra Information to the Step**

You can add any additional information to the step using `add_extra_info`. A step can have multiple `add_extra_info` calls.

```python
# Add extra information to the step
step1.add_extra_info("Query", "What is the status of order #12345?")
step1.add_extra_info("RetrievedData", {"order_status": "Shipped", "delivery_date": "2024-10-05"})
```

#### **3. Register Errors or Warnings (If Any)**

If an error occurs during the step, you can log it using `add_error`.

```python
from enola.enola_types import ErrOrWarnKind

# Register an error in the step
step1.add_error(
    id="E001",
    message="Failed to connect to the database",
    kind=ErrOrWarnKind.INTERNAL_CONTROLLED
)
```

Similarly, you can register warnings using `add_warning`.

```python
# Register a warning in the step
step1.add_warning(
    id="W001",
    message="Data retrieval took longer than expected",
    kind=ErrOrWarnKind.EXTERNAL
)
```

---

### Closing Steps

After performing the necessary operations in a step, you need to close it. The way you close a step depends on the type of step.

#### **Closing a Generic Step**

```python
# Close the generic step
monitor.close_step_others(
    step=step1,
    successfull=True,  # Set to True if the step was successful
    message_output="Data retrieval completed successfully."
)
```

#### **Closing a Token-based Step (e.g., LLM Processing)**

If your step involves processing with a language model (LLM), you might want to track token usage and costs.

```python
# Create an LLM processing step
step2 = monitor.new_step("LLM Inference Step")

# Add input message
step2.add_extra_info("UserQuestion", "What is the status of order #12345?")

# Simulate model processing and get output
model_output = "Your order #12345 has been shipped and will arrive on 2024-10-05."

# Add output message
step2.add_extra_info("ModelResponse", model_output)

# Close the LLM step with token information
monitor.close_step_token(
    step=step2,
    successfull=True,
    message_output=model_output,
    token_input_num=50,    # Number of input tokens
    token_output_num=20,   # Number of output tokens
    token_total_num=70,    # Total tokens used
    token_input_cost=0.005,  # Cost for input tokens
    token_output_cost=0.002, # Cost for output tokens
    token_total_cost=0.007  # Total cost
)
```

---

### Finalizing and Sending Data to the Server

After completing all steps, you need to finalize the tracking session and send the data to the Enola AI server.

```python
# Finalize tracking and send data to the server
monitor.execute(
    successfull=True,  # Set to True if the entire session was successful
    message_output="Session completed successfully.",
    num_iteratons=2    # Number of iterations or steps in the session
)
```

---

### Complete Example

Here's how all the pieces come together:

```python
import os
from enola.tracking import Tracking
from enola.enola_types import ErrOrWarnKind

# Set up your token
token = os.getenv('ENOLA_TOKEN')

# Initialize the tracking agent
monitor = Tracking(
    token=token,
    name="Customer Support Session",
    is_test=False,
    user_id="customer_001",
    user_name="Alice Smith",
    app_id="support_app",
    app_name="Customer Support App",
    channel_id="live_chat",
    channel_name="Live Chat",
    session_id="session_789",
    session_name="Support Session 789",
    message_input="I need help with my order."
)

# Step 1: Data Retrieval
step1 = monitor.new_step("Data Retrieval Step")
step1.add_extra_info("Query", "What is the status of order #12345?")
# Simulate data retrieval
retrieved_data = {"order_status": "Shipped", "delivery_date": "2024-10-05"}
step1.add_extra_info("RetrievedData", retrieved_data)
# Close the step
monitor.close_step_others(
    step=step1,
    successfull=True,
    message_output="Data retrieval completed successfully."
)

# Step 2: LLM Inference
step2 = monitor.new_step("LLM Inference Step")
step2.add_extra_info("UserQuestion", "What is the status of order #12345?")
# Simulate model processing and get output
model_output = "Your order #12345 has been shipped and will arrive on 2024-10-05."
step2.add_extra_info("ModelResponse", model_output)
# Close the step with token usage
monitor.close_step_token(
    step=step2,
    successfull=True,
    message_output=model_output,
    token_input_num=50,
    token_output_num=20,
    token_total_num=70,
    token_input_cost=0.005,
    token_output_cost=0.002,
    token_total_cost=0.007
)

# Finalize tracking and send data to the server
monitor.execute(
    successfull=True,
    message_output="Session completed successfully.",
    num_iteratons=2
)
```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or corrections.

When contributing, please ensure to:

- Follow the existing coding style.
- Write clear commit messages.
- Update documentation as necessary.
- Ensure that any code changes are covered by tests.

---

## License

This project is licensed under the **BSD 3-Clause License**. See the [LICENSE](LICENSE) file for more details.

---

## Contact

For any inquiries or support, please contact us at [help@huemulsolutions.com](mailto:help@huemulsolutions.com).

---

## Additional Information

- **API Reference**: For detailed documentation of all classes and methods, please refer to the [Enola AI SDK API Reference](docs/api_reference.md).
- **Examples**: Additional examples can be found in the [examples](examples) directory.
- **FAQ**: Frequently Asked Questions are answered in the [FAQ](docs/FAQ.md) section.

---

## Documentation

For project documentation, please visit our [Enola AI Documentation](https://marceloxofh.github.io/preview-enola-doc/docs/).

---

## Suggestions and Next Steps

- **Expand Examples**: As you become more familiar with the Enola AI SDK, consider exploring advanced topics like batch processing, error handling, and performance optimization.
- **Integrate with Your Applications**: Leverage the Enola AI SDK to enhance observability and compliance in your AI applications.
- **Provide Feedback**: Your feedback helps us improve. Please share your thoughts, suggestions, and experiences with us.