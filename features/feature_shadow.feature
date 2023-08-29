Feature: Use a shadow mode

    An feature flagged with a shadow feature flag should be able to execute the original
    method/function and the new feature. This enables the user, to not finish the new feature
    and use the old method/function in the mean time. The flag itself gets the old function/method
    as an input. The new method can either run with the same parameters as the old function, either after
    the old function or in parallel -> that is the so called shadow flag. Or the new method/function
    is disabled and only the old function is used.

    Background: Class with several methods is available
        Given there is a class with a method_old and takes an string as an input
        Given that the method_old returns the input string when called
        Given in this class is a method_new with arbitrary arguments
        Given that method_new raises a exception when directly called

    Scenario: Flagging the method_new as a shadow function
        When method_new gets the flag feature_flag.shadow(run=method_old)
        Then when method_new is called with an input string it returns the input string
