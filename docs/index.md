# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)
## Custom Project

### Dataset
I used the system metrics time-series dataset included in the project. The dataset contains timestamps, requests, errors, and total latency in milliseconds. Each row represents one observation at a specific point in time.

### Signals
I used the original rolling mean signals for requests, errors, and latency. I also created three new signals: error_rate, latency_rolling_max, and high_error_flag. These signals help show how the system behaves over time and make it easier to identify possible problems.

### Experiments
I created a new Python file called rolling_monitor_abdellah.py and kept the original documentation from the example. Then I added new derived monitoring signals to extend the original project without changing the example file itself.

### Results
The rolling mean signals smoothed the short-term variation in the data. The error_rate column helped show the relationship between errors and requests, and the high_error_flag column highlighted periods where the error rate was above the threshold. The rolling maximum latency also made it easier to see recent high-latency values.

### Interpretation
This project shows that rolling monitoring can help an analyst understand system behavior more clearly. Instead of only reading raw values, it is possible to use rolling signals and derived indicators to detect patterns, monitor risk, and support better decisions.
