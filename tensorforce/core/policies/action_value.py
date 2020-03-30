# Copyright 2018 Tensorforce Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from collections import OrderedDict

import tensorflow as tf

from tensorforce import util
from tensorforce.core import tf_function
from tensorforce.core.policies import Policy


class ActionValue(Policy):
    """
    Base class for action-value-based policies.

    Args:
        device (string): Device name
            (<span style="color:#00C000"><b>default</b></span>: inherit value of parent module).
        summary_labels ('all' | iter[string]): Labels of summaries to record
            (<span style="color:#00C000"><b>default</b></span>: inherit value of parent module).
        l2_regularization (float >= 0.0): Scalar controlling L2 regularization
            (<span style="color:#00C000"><b>default</b></span>: inherit value of parent module).
        name (string): <span style="color:#0000C0"><b>internal use</b></span>.
        states_spec (specification): <span style="color:#0000C0"><b>internal use</b></span>.
        auxiliaries_spec (specification): <span style="color:#0000C0"><b>internal use</b></span>.
        actions_spec (specification): <span style="color:#0000C0"><b>internal use</b></span>.
    """

    def input_signature(self, function):
        if function == 'actions_value':
            return [
                util.to_tensor_spec(value_spec=self.states_spec, batched=True),
                util.to_tensor_spec(value_spec=dict(type='long', shape=(2,)), batched=True),
                util.to_tensor_spec(value_spec=self.internals_spec(policy=self), batched=True),
                util.to_tensor_spec(value_spec=self.auxiliaries_spec, batched=True),
                util.to_tensor_spec(value_spec=self.actions_spec, batched=True)
            ]

        elif function == 'actions_values':
            return [
                util.to_tensor_spec(value_spec=self.states_spec, batched=True),
                util.to_tensor_spec(value_spec=dict(type='long', shape=(2,)), batched=True),
                util.to_tensor_spec(value_spec=self.internals_spec(policy=self), batched=True),
                util.to_tensor_spec(value_spec=self.auxiliaries_spec, batched=True),
                util.to_tensor_spec(value_spec=self.actions_spec, batched=True)
            ]

        elif function == 'states_value':
            return [
                util.to_tensor_spec(value_spec=self.states_spec, batched=True),
                util.to_tensor_spec(value_spec=dict(type='long', shape=(2,)), batched=True),
                util.to_tensor_spec(value_spec=self.internals_spec(policy=self), batched=True),
                util.to_tensor_spec(value_spec=self.auxiliaries_spec, batched=True)
            ]

        elif function == 'states_values':
            return [
                util.to_tensor_spec(value_spec=self.states_spec, batched=True),
                util.to_tensor_spec(value_spec=dict(type='long', shape=(2,)), batched=True),
                util.to_tensor_spec(value_spec=self.internals_spec(policy=self), batched=True),
                util.to_tensor_spec(value_spec=self.auxiliaries_spec, batched=True)
            ]

        else:
            return super().input_signature(function=function)

    @tf_function(num_args=4)
    def act(self, states, horizons, internals, auxiliaries):
        raise NotImplementedError

    @tf_function(num_args=5)
    def actions_value(
        self, states, horizons, internals, auxiliaries, actions, reduced, return_per_action
    ):
        actions_values = self.actions_values(
            states=states, horizons=horizons, internals=internals, auxiliaries=auxiliaries,
            actions=actions
        )

        return self.join_value_per_action(
            values=actions_values, reduced=reduced, return_per_action=return_per_action
        )

    @tf_function(num_args=4)
    def states_value(self, states, horizons, internals, auxiliaries, reduced, return_per_action):
        states_values = self.states_values(
            states=states, horizons=horizons, internals=internals, auxiliaries=auxiliaries
        )

        return self.join_value_per_action(
            values=states_values, reduced=reduced, return_per_action=return_per_action
        )

    @tf_function(num_args=5)
    def actions_values(self, states, horizons, internals, auxiliaries, actions):
        raise NotImplementedError

    @tf_function(num_args=4)
    def states_values(self, states, horizons, internals, auxiliaries):
        raise NotImplementedError
