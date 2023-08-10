Feature: Named feature flags

    Provide a name via a feature flag to group several methods/functions/classes together. Disable/Enable all at once.

    Background:
        Given There is a method called method_a which returns 'method a'
        Given There is a method called method_b which returns 'method b'

    Scenario: Provide a name and deactivate feature
        When a feature flag contains a name and is added with feature.flag('off', name='not_working_feature') to method_a
        Then if a feature flag is added to method_b with feature.flag(name='not_working_feature')
        Then if method_b is called a 'NotImplementedError' exception is raised

    Scenario: Activate a named feature
        Given that method_a has been flagged with feature.flag('on', name='be_activated')
        Given that method_b has been flagged with feature.flag(name='be_activated')
        When method_a is called and returns 'method_a'
        Then method_b is called it returns 'method b'

    Scenario: Deactivated method with response only with method a
        Given that method_a has been flagged with feature.flag('off', name='deactivated_with_response', response='I am method a')
        Given that method_b has been flagged with feature.flag(name='deactivated_with_response')
        When method_a is called and returns 'I am method a'
        Then method_b is called it raises 'NotImplementedError'

    Scenario: Deactivated method with response with both methods
        Given that method_a has been flagged with feature.flag('off', name='deactivated_with_response', response='I am method a')
        Given that method_b has been flagged with feature.flag(name='deactivated_with_response', name='I am method b')
        When method_a is called and returns 'I am method a'
        Then method_b is called and returns 'I am method b'
