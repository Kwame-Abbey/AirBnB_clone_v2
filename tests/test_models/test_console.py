#!/usr/bin/python3
"""test for console """
import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import json
import console
import tests
from models import storage
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Place
from models.review import Review
from models.engine.file_storage import FileStorage

class TestConsole(unittest.TestCase):
    """ this tests the console"""

    @classmethod
    def setUpClass(cls):
        """ setup for the test """
        cls.consol = HBNBCommand()


    @classmethod
    def teardown(cls):
        """ tears down at the end of the test """
        del cls.consol


    def tearDown(self):
        """ Remove temporary file(file.json) created as a result """
        try:
            os.remove("file.json")
        except Exception:
            pass


    def test_pep8_console(self):
        """ Perp8 console """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')


    def tets_docstrins_in_console(self):
        """ checks for docstrings """
        self.asserIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)


    def test_emptyline(self):
        """ Tests empty line input """
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())


    def tets_quit(self):
        """ Tests create command input """
        with patch('sys.stdout', new=StringIO()) as f:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create")
                self.assertEqual(
                        "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertEqual(
                "[[User]", f.getvalue()[:7])

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create State name="California"\
            lat=7.5 zip=513')
            id = f.getvalue().strip("\n")
        alldic = storage.all()
        clas = "State."
        Sname = alldic[clas + id].name
        Slat = alldic[clas + id].lat
        Szip = alldic[clas + id].zip
        self.assertEqual(Sname, "California")
        self.assertTrue(isinstance(Sname, str))
        self.assertEqual(Slat, 7.5)
        self.assertTrue(isinstance(Slat, float))
        self.assertEqual(Szip, 513)
        self.assertTrue(isinstance(Szip, int))

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd('create User name="Larry_Moon"\
            nik="El\\"Macho"')
            id = f.getvalue().strip("\n")
        alldic = storage.all()
        clas = "User."
        Sname = alldic[clas + id].name
        Snick = alldic[clas + id].nik
        self.assertEqual(Sname, "Larry Moon")
        self.assertTrue(isinstance(Sname, str))
        self.assertEqual(Snick, 'El"Macho')
        self.assertTrue(isinstance(Snick, str))


    def test_show(self):
        """ Tests show command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show")
            self.assertEqual(
                    "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show asdfsdrfs")
            self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel")
            self.assertEqual(
                     "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                    "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """ Tests destroy command input """
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEquual(
                 "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all(self):
        """ Tests all command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())


    def test_update(self):
        """ Tests update command input """
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update sldkfjsl")
            self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())




if __name__ == "__main__":
    
    unittest.main()
