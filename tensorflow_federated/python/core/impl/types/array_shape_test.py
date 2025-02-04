# Copyright 2023, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from absl.testing import absltest
from absl.testing import parameterized

from tensorflow_federated.python.core.impl.types import array_shape


class ArrayShapeTest(parameterized.TestCase):

  @parameterized.named_parameters(
      ('fully_defined', (2, 3)),
      ('scalar', ()),
  )
  def test_is_shape_fully_defined_returns_true(self, shape):
    result = array_shape.is_shape_fully_defined(shape)
    self.assertTrue(result)

  @parameterized.named_parameters(
      ('partially_defined', (2, None)),
      ('unknown', None),
  )
  def test_is_shape_fully_defined_returns_false(self, shape):
    result = array_shape.is_shape_fully_defined(shape)
    self.assertFalse(result)

  def test_is_shape_scalar_returns_true(self):
    shape = ()
    result = array_shape.is_shape_scalar(shape)
    self.assertTrue(result)

  @parameterized.named_parameters(
      ('fully_defined', (2, 3)),
      ('partially_defined', (2, None)),
      ('unknown', None),
  )
  def test_is_shape_scalar_returns_false(self, shape):
    result = array_shape.is_shape_scalar(shape)
    self.assertFalse(result)

  @parameterized.named_parameters(
      ('unknown_and_fully_defined', None, (2, 3)),
      ('unknown_and_partially_defined', None, (2, None)),
      ('unknown_and_unknown', None, None),
      ('unknown_and_scalar', None, ()),
      ('known_dimensions_and_fully_defined', (None, None), (2, 3)),
      ('known_dimensions_and_partially_defined', (None, None), (2, None)),
      ('known_dimensions_and_unknown', (None, None), None),
      ('partially_defined_and_fully_defined', (2, None), (2, 3)),
      ('partially_defined_and_partially_defined', (2, None), (2, None)),
      ('partially_defined_and_unknown', (2, None), None),
      ('fully_defined_and_fully_defined', (2, 3), (2, 3)),
      ('fully_defined_and_partially_defined', (2, 3), (2, None)),
      ('fully_defined_and_unknown', (2, 3), None),
  )
  def test_is_compatible_with_returns_true(self, target, other):
    result = array_shape.is_compatible_with(target, other)
    self.assertTrue(result)

  @parameterized.named_parameters(
      ('known_dimensions_and_scalar', (None, None), ()),
      ('known_dimensions_wrong_length_short', (None, None), (None,)),
      ('known_dimensions_wrong_length_long', (None, None), (None, None, None)),
      ('partially_defined_and_scalar', (2, None), ()),
      ('partially_defined_wrong_size', (2, None), (20, None)),
      ('fully_defined_and_scalar', (2, 3), ()),
      ('fully_defined_wrong_size', (2, 3), (20, 3)),
  )
  def test_is_compatible_with_returns_false(self, target, other):
    result = array_shape.is_compatible_with(target, other)
    self.assertFalse(result)

  @parameterized.named_parameters(
      ('fully_defined', (2, 3), 6),
      ('partially_defined', (2, None), None),
      ('unknown', None, None),
      ('scalar', (), 1),
  )
  def test_num_elements_in_shape_returns_result(self, shape, expected_result):
    actual_result = array_shape.num_elements_in_shape(shape)
    self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
  absltest.main()
