Feature: Feature configuration file

    All feature flags should be configurable via a feature flag configuration file.
    Feature flags can be loaded by this configuration file. This feature configuration file is written
    in the `toml` format. Every feature contains the name as the header. It also contains
    the status `active` - which assumes that in capital written names are environment
    variables containing the activation status. The default path of the configuration file
    is the root directory of the package. E.g. the same as the `pyproject.toml`

    Background: Configuration file and methods
        Given there is a configuration file containing feature flag 'feature_method_a', 'feature_method_b' and 'feature_method_c'
        Given 'feature_method_a' contains the activation 'on'
        Given 'feature_method_b' contains the activation 'off'
        Given 'feature_method_c' contains the activation 'FEATURE_METHOD_C'
        Given there is a method_a which returns 'method a'
        Given there is a method_b which returns 'method b'
        Given there is a method_c which returns 'method c'

    Scenario: Load active feature by configuration
        When method_a gets the flag feature_flag(name='feature_method_a')
        Then when method_a is called it returns 'method a'

    Scenario: Load inactive feature by configuration
        When method_b gets the flag feature_flag(name='feature_method_b')
        Then when method_b is called it raises a NotImplementedError

    Scenario: Overrule feature flag activation by configuration
        When method_a gets the flag feature_flag('off', name='feature_method_a')
        Then when overruled method_a is called it returns 'method a'

    Scenario: Activate feature by environment variable
        When the environment variable 'FEATURE_METHOD_C' contains 'on'
        Then when method_c gets the flag feature_flag(name='feature_method_c')
        Then when method_c is called it returns 'method c'

    Scenario: Inactive feature by environment variable
        When the environment variable 'FEATURE_METHOD_C' contains 'off'
        Then when inactive method_c gets the flag feature_flag(name='feature_method_c')
        Then when method_c is called it raises NotImplementedError
