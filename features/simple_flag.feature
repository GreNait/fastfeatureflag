Feature: Simple feature flag

    Add a simple feature flag to a function/method disabling the function/method.

    Background:
        Given There is a method called disable

    Scenario: A feature flag is added to disable the function
        When a feature flag feature.flag('off') is added
        Then if I try to call the method a 'NotImplementedError' exception is raised

    Scenario Outline: A feature flag is added to disable the function which returns True|False
        When a feature flag feature.flag("off", response="<response_in>") is added
        Then if I call the method it returns "<response_out>"

        Examples: Response
            | response_in | response_out |
            | True        | True         |
            | False       | False        |
            | Something | Something  |
