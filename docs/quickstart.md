# Quickstart

# TL;DR

```python
from fastfeatureflag.feature_flag import feature_flag

@feature_flag(activation="off", response="I responded")
def not_yet_finished_feature():
    return True

print(not_yet_finished_feature())
I responded

@feature_flag("on")
def not_yet_finished_feature():
    return True
not_yet_finished_feature()
True

@feature_flag("off", name="awesome_feature", response="Not finished yet")
def awesome_feature_1():
    return "I am feature 1"

@feature_flag(name="awesome_feature", response="Not finished yet")
def awesome_feature_2():
    return "I am feature 2"

awesome_feature_1()
awesome_feature_2()
'Not finished yet'

@feature_flag("on", name="awesome_feature")
def awesome_feature_1():
    return "I am feature 1"

@feature_flag("off", name="awesome_feature")
def awesome_feature_2():
    return "I am feature 2"

awesome_feature_1()
awesome_feature_2()
---------------------------------------------------------------------------
NotImplementedError                       Traceback (most recent call last)
Cell In[10], line 11
      7 @feature_flag("off", name="awesome_feature")
      8 def awesome_feature_2():
      9     return "I am feature 2"
---> 11 awesome_feature_1()
```

## Import feature flag

```python
from fastfeatureflag.feature_flag import feature_flag
```

## Adding a feature flag

By adding `feature_flag()` to a method, the method will raise an `NotImplementedError` if called.

=== "unflagged"

    ```python
    def not_yet_finished_feature():
        ...
    ```

=== "flagged"

    ```python
    @feature_flag()
    def not_yet_finished_feature():
        ...
    ```

??? note "You can specify the activation of a feature flag"

    ```python
    @feature_flag(activation="off")
    ```

    `feature_flag()` equals `feature_flag("off")`

By adding the feature without any parameters, it will disable the method/function/class.

## Respond even if deactive

Sometimes a feature should be callable, but respond with a different response. Because it might not be finished yet, but other parts want to interact with it already. Providing a response to the feature flag can solve this issue.

=== "unflagged"

    ```python
    >>> def not_yet_finished_feature():
    ...     return True
    >>> not_yet_finished_feature()
    True
    ```

=== "flagged"

    ```python
    >>> @feature_flag(response="I responded")
    ... def not_yet_finished_feature():
    ...     return True
    >>> not_yet_finished_feature()
    'I responded'
    ```

## Activate a feature

If you want a flagged method/function/class to be active, configure the flag to be active.

=== "flagged"

    ```python
    >>> @feature_flag("on")
    ... def not_yet_finished_feature():
    ...     return True
    ...
    >>> not_yet_finished_feature()
    True
    ```

## Name a feature

### Deactive

If you have several methods/functions you want to group, use a name for that feature.

=== "feature 1"

    ```python
    >>> @feature_flag("off", name="awesome_feature", response="Not finished yet")
    ... def awesome_feature_1():
    ...     return "I am feature 1"
    ...
    ```

=== "feature 2"

    ```python
    >>> @feature_flag(name="awesome_feature", response="Not finished yet")
    ... def awesome_feature_2():
    ...     return "I am feature 2"
    ...
    ```

=== "calling both features"

    ```python
    >>> awesome_feature_1()
    'Not finished yet'
    >>> awesome_feature_2()
    'Not finished yet'
    ```

These methods are now registered as a feature and changing the activation to "on" in the feature flag changes the activation for all flagged objects.

### Active

!!! tip "Typically the `feature_flag(name="named_feature")` flag would assume an `off` activation. However, as a group they share the activation."

Activate the feature by changing from `off` to `on` in the activation.

=== "feature 1"

    ```python
    >>> @feature_flag("on", name="awesome_feature")
    ... def awesome_feature_1():
    ...     return "I am feature 1"
    ...
    ```

=== "feature 2"

    ```python
    >>> @feature_flag(name="awesome_feature")
    ... def awesome_feature_2():
    ...     return "I am feature 2"
    ...
    ```

=== "calling both features"

    ```python
    >>> awesome_feature_1()
    'I am feature 1'
    >>> awesome_feature_2()
    'I am feature 2'
    ```

!!! note "The first activation wins"

    If you have several objects flagged with with the same name and different `activations`, then the first activation wins. The first flag registers the name and activation. Any other flag will not change the already registered feature.

    ??? tip "Cleaning the feature register"

        It is possible to clean all already registered features and update the configuration of all features.

        ```python
        from fastfeatureflag.feature_flag import feature_flag
        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        @feature_flag(name="test_clean_register", response="I am deactivated")
        def broken_feature():
            return "I am broken"

        pp.pprint(broken_feature())

        pp.pprint(broken_feature.registered_features)
        broken_feature.clean()

        pp.pprint(broken_feature.registered_features)
        pp.pprint(broken_feature())
        ```
        Output:
        ```console
        'I am deactivated'
        [   FeatureContent(activation='off',
                        name='test_clean_register',
                        response=None,
                        shadow=None,
                        func=<function broken_feature at 0x7fea25881ea0>,
                        configuration=None,
                        configuration_path=None)]
        []
        'I am deactivated'
        ```

        Be aware, that this only "unregister" a feature. It does not deactivate it. Meaning, e.g. a configured response is still forwarded.
        If you want to change and register new features dynamically, you can provide the feature configuration:

        ```python
        from fastfeatureflag.feature_flag import feature_flag
        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        @feature_flag(name="test_clean_register", response="I am deactivated")
        def broken_feature():
            return "I am broken"

        pp.pprint(broken_feature())

        configuration = {"test_clean_register" : {"activation":"off", "response":"I am re-configured"}}
        broken_feature.configuration = configuration
        pp.pprint(broken_feature.configuration)

        broken_feature()
        ```
        Output:
        ```console
        'I am deactivated'
        {'test_clean_register': {'activation': 'off', 'response': 'I am re-configured'}}
        'I am re-configured'
        ```

!!! tip "Every flagged method has its own unique response"

    If you want that a deactivated object returns a custom response, you will have to define one and provide it to every feature flag individually.

## Use a configuration file

Handling several features and their activation manually with every flag might lead to conflicting activations and responses. To manage them, you can use a configuration file. As a default, all feature flags are searching for a `fastfeatureflag_config.toml` within the current working directory.

Within this configuration file, you can easily specify the features (as `titles`) and their activation.

```toml title="fastfeatureflag_config.toml"
[feature_1]
activation="on"

[feature_2]
activation="off"
```

This file provides you a central location to switch off/on the features you need. Another great option is the use of environment variables within the activation.

```toml title="fastfeatureflag_config.toml"
[feature_1]
activation="FEATURE_1"
```

By providing the name of the environment variable it is possible to read their status. You can now switch on/off the feature by providing "on"|"off" via the environment variable.

```bash
export FEATURE_1 = "on"
```

In combination with `.env` files, you can save and specify the features for your local use case. Provide different `.env` files or other means of environment variables to easily handle feature flags within a `CI/CD` pipeline too.

??? tip "Environment variable standard"

    Typically, environment variables are written in `upper case`. However, the feature flag system searches for every word as an environment variable. Take also care, that no environment variable with the key words `on` and `off` have been defined.
