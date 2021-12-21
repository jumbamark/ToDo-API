from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ToDos.models import ToDo


class ToDosAPITestCase(APITestCase):
    def authenticate(self):
        self.client.post(reverse('register'), {"username": "username", "email": "email@gmail.com", "password": "password"})
        response = self.client.post(reverse('login'), {"email": "email@gmail.com", "password": "password"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")


    def create_todo(self):
        sample_todo = {"title": "17th January of 2022", "description": "End of semester exams"}
        response = self.client.post(reverse("to-dos"),sample_todo)

        return response



# Create your tests here.
class TestListCreateToDos(ToDosAPITestCase):

    def test_should_not_create_to_do_with_no_authentication(self):
        # sample_todo = {"title": "17th January of 2022", "description": "End of semester exams"}
        # response = self.client.post(reverse("to-dos"),sample_todo)
        response = self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_to_do(self):
        previous_todo_count = ToDo.objects.all().count()
        self.authenticate()
        # sample_todo = {"title": "21st December of 2021", "description": "Finish DRF course"}
        # response = self.client.post(reverse("to-dos"),sample_todo)
        response = self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDo.objects.all().count(), previous_todo_count+1)
        self.assertEqual(response.data["title"], "17th January of 2022")
        self.assertEqual(response.data["description"], "End of semester exams")
    
    # test that can retrieve all items
    def test_retrieve_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse("to-dos"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data["results"],list)

        # whenever we create we get the pagination stuff
        response = self.create_todo()
        # sample_todo = {"title": "17th January of 2022", "description": "End of semester exams"}
        # self.client.post(reverse("to-dos"),sample_todo)

        response = self.client.get(reverse("to-dos"))
        self.assertIsInstance(response.data["count"],int)
        self.assertEqual(response.data["count"], 1)  # check that it's one


# testing that we can view a to-do, we can be able to edit and delete it
class TestToDoDetailAPIView(ToDosAPITestCase):

    def test_retrieve_one_item(self):
        self.authenticate()
        response = self.create_todo()
        res = self.client.get(reverse("to-do", kwargs={"id": response.data["id"]}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # check whetehr the one send to us is the one in the db
        todo = ToDo.objects.get(id=response.data["id"])
        self.assertEqual(todo.title, res.data["title"])   # assert that tile = title in the res

    
    def test_updates_one_item(self):
        self.authenticate()
        response = self.create_todo()

        res = self.client.patch(reverse("to-do", kwargs={"id": response.data["id"]}), {"title": "updated title", "is_complete": True})
        # confirm that the db updated and the view responded succesfully
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        update_todo = ToDo.objects.get(id=response.data["id"])
        self.assertEqual(update_todo.is_complete, True)
        self.assertEqual(update_todo.title, "updated title")

    # authenticate a user, create_todo,check the database has a specific no of items, delete a todo and check the number of items reduced
    def test_deletes_one_item(self):
        self.authenticate()
        res = self.create_todo()
        previous_db_count = ToDo.objects.all().count()

        self.assertGreater(previous_db_count, 0)
        self.assertEqual(previous_db_count, 1)

        response = self.client.delete(reverse('to-do', kwargs={'id': res.data["id"]}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ToDo.objects.all().count(), 0)