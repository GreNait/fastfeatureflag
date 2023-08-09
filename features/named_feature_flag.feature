Feature: Named feature flags

    Provide a name via a feature flag to group several methods/functions/classes together. Disable/Enable all at once.

    Background:
        Given There is a method called method_a
        Given There is a method called method_b

    Scenario: Provide a name and deactivate feature
        When a feature flag contains a name and is added with feature.flag('off', name='not_working_feature') to method_a
        Then if a feature flag is added to method_b with feature.flag(name='not_working_feature')
        Then if method_b is called a 'NotImplementedError' excpetion is raised

    Scenario: Activate a named feature
        Given that method_a has been flaged with feature.flag('on', name='be_activated', response='got_called')
        Given that method_b has been flaged with feature.flag(name='be_activated')
        When method_b is called it returns 'got_called'
