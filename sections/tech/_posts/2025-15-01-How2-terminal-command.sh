---
layout: post
title: Creating the How2 Function for Natural Language Bash Commands with LLM
date: 2025-01-15
categories: tech
---

In today's tech-driven world, the ability to translate natural language into executable commands is a powerful tool for developers and system administrators alike. Recently, I embarked on creating a function that bridges this gap using a Large Language Model (LLM) to interpret user queries in natural language and return the corresponding Bash terminal commands. Here's how I constructed the `how2` function that provides users with Bash commands based on their queries.
The trick is to use the fantastic LLM-CLI command by Simon Wilson [llm](https://llm.datasette.io).
Then one needs to wrap the calls to LLM into a specific bash function called `how2`.

## The Concept

The main idea behind the `how2` function is simple: allow users to input their requests in a natural language format, and then leverage the capabilities of an LLM to retrieve the relevant Bash command. This eliminates the need to remember complex syntax or search for answers online while working in the terminal.

## The Implementation

Here’s the complete code for the function:

```bash
how2() {
  if [ $# -eq 0 ]; then
    echo "Usage: how2 <query>"
    return 1
  fi

  # Concatenate the query arguments into a single string
  query="$*"
  system_prompt="You are a bash shell script super expert. Write ONLY the bash shell command answering the question. Ensure to always enclose the output between triple backticks in a single line command."

  # Capture the output from llm command
  output=$(llm -s "$system_prompt" "Question:\n$query\nAnswer:")

  # Use a modified regex pattern that handles multiline content
  if [[ "$output" =~ [[:space:]]*\`\`\`[[:space:]]*(.|\n)*[[:space:]]*\`\`\`[[:space:]]* ]]; then
    # Extract content between backticks, removing the first and last line if they only contain backticks
    content=$(echo "$output" | sed -n '/^```/,/^```/ p' | sed '1d;$d')

    # Output the result in blue color
    echo -e "\e[34m$content\e[0m"
  else
    echo "No valid response with triple backticks found!" >&2
  fi
}
```

## Breaking Down the Function

### Argument Handling
The first step in the function is to check if any query has been provided. If no arguments are supplied, the user is reminded of the proper usage.

### Concatenating the Query
Next, all input arguments are concatenated into a single string, making it easier to interpret the user's intent as a natural language question.

### Constructing the System Prompt
A system prompt is crafted to instruct the LLM about its role. In this case, the model is guided to act as a "bash shell script super expert." This prompt is key, as it sets the expectations for the output format.

### Querying the LLM
With both the concatenated query and the system prompt in hand, the function then calls the LLM using the `llm` command. The output from this command contains the model's interpretation of the query.

## Examples

```bash
how2 list all the files in .txt format in reverse alphabetic order?
```

### Extracting the Bash Command
The output returned by the LLM is examined for content enclosed in triple backticks, which signifies the desired command. This step uses a regex pattern that accommodates multiline responses but ensures that we capture only the valid command.

### Output Formatting
Finally, the extracted command is printed in blue color for better visibility in the terminal. If no valid command is found, an error message is displayed.

## Conclusion

Creating the `how2` function has not only enhanced my workflow but also made Bash scripting more accessible to those who may not be familiar with command-line intricacies. By leveraging the capabilities of an LLM, we can effectively translate natural language into actionable commands. This tool can be particularly beneficial for beginners or anyone looking to streamline their command-line experience.

Feel free to customize and enhance this function further to fit your specific needs, and happy scripting!
