from unittest import TestCase, main
from main import Department, Employee, Manager, Seller


class TestDepartament(TestCase):

    def test_create_department(self):
        dep = Department('vendas', 1)
        self.assertEqual('vendas', dep.name)
        self.assertEqual(1, dep.code)

    def test_create_department_should_return_error(self):
        with self.assertRaises(TypeError):
            Department()


class TestAbstractEmployee(TestCase):

    def test_could_not_instantiate_abstract_employee(self):
        with self.assertRaises(TypeError):
            Employee(123, 'João da Silva', 2500.0)


class TestManager(TestCase):

    def setUp(self):
        self._manager = Manager(1, 'João da Silva', 4000.0)

    def test_create_manager(self):
        self.assertEqual(1, self._manager.code)
        self.assertEqual('João da Silva', self._manager.name)
        self.assertEqual(4000.0, self._manager.salary)

    def test_manager_calc_bonus(self):
        expected = 4000.0*0.15
        self.assertEqual(expected, self._manager.calc_bonus())

    def test_manager_get_hours_should_return_8(self):
        self.assertEqual(8, self._manager.get_hours())

    def test_manager_get_department_should_return_mananagers(self):
        self.assertEqual('managers', self._manager.get_department())

    def test_manager_set_department_should_update_department(self):
        self.assertEqual('managers', self._manager.get_department())
        
        new_departament = 'sellers'
        self._manager.set_departament(new_departament)
        self.assertEqual(new_departament, self._manager.get_department())


class TestSeller(TestCase):

    def setUp(self):
        self._seller = Seller(1, 'João da Silva', 3000.0)

    def test_create_seller(self):
        self.assertEqual(1, self._seller.code)
        self.assertEqual('João da Silva', self._seller.name)
        self.assertEqual(3000.0, self._seller.salary)

    def test_seller_get_hours_should_return_8(self):
        self.assertEqual(8, self._seller.get_hours())

    def test_seller_get_sales_should_return_0(self):
        self.assertEqual(0, self._seller.get_sales())

    def test_seller_get_sales_should_return_800(self):
        self._seller.put_sales(800)
        self.assertEqual(800, self._seller.get_sales())

    def test_seller_get_department_should_return_sellers(self):
        self.assertEqual('sellers', self._seller.get_department())

    def test_seller_set_department_should_update_department(self):
        self.assertEqual('sellers', self._seller.get_department())
        
        new_department = 'managers'
        self._seller.set_departament(new_department)
        self.assertEqual(new_department, self._seller.get_department())

    def test_seller_calc_bonus(self):
        expected = 800.0*0.15
        
        self._seller.put_sales(800)
        self.assertEqual(expected, self._seller.calc_bonus())
    

if __name__ == "__main__":
    main()
