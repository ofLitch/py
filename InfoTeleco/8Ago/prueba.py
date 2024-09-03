import json
import mysql.connector

class Math(object):
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
        self.operation = ""
        self.result = 0
        
    def add(self):
        self.operation = "Suma"
        self.result = self.value1 + self.value2
        return self.result
    
    def subtract(self):
        self.operation = "Resta"
        self.result = self.value1 - self.value2
        return self.result
    
    def multiply(self):
        self.operation = "Multiplicación"
        self.result = self.value1 * self.value2
        return self.result
    
    def divide(self):
        self.operation = "División"
        self.result = self.value1 / self.value2
        return self.result
    
    def set_values(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
    
class DB(object):
    def __init__(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='infoteleco'
            )
            if connection.is_connected():
                print("Conexión exitosa a la base de datos")
                self.connection = connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None
    
    def generate_json(self, math_instance):
        data = {
            "operation": math_instance.operation,
            "value1": math_instance.value1,
            "value2": math_instance.value2,
            "result": math_instance.result
        }
        with open("result.json", "w") as file:
            json.dump(data, file)
        print("Archivo JSON generado con éxito")
    
    def store_in_db(self, math_instance):
        if self.connection is not None:
            cursor = self.connection.cursor()
            query = "INSERT INTO math_operations (operation, value1, value2, result) VALUES (%s, %s, %s, %s)"
            values = (math_instance.operation, math_instance.value1, math_instance.value2, math_instance.result)
            cursor.execute(query, values)
            self.connection.commit()
            print("Datos almacenados exitosamente en la base de datos")
        else:
            print("No hay conexión con la base de datos")


def menu():
    print("\nMenú de Operaciones:")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Generar JSON")
    print("6. Almacenar en la base de datos")
    print("7. Salir")
    return input("Selecciona una opción: ")


db = DB()

value1 = float(input("Ingrese el primer valor: "))
value2 = float(input("Ingrese el segundo valor: "))
math_instance = Math(value1, value2)

while True:
    option = menu()
    
    if option == '1':
        result = math_instance.add()
        print(f"Resultado de la suma: {result}")
    
    elif option == '2':
        result = math_instance.subtract()
        print(f"Resultado de la resta: {result}")
    
    elif option == '3':
        result = math_instance.multiply()
        print(f"Resultado de la multiplicación: {result}")
    
    elif option == '4':
        result = math_instance.divide()
        print(f"Resultado de la división: {result}")
    
    elif option == '5':
        db.generate_json(math_instance)
    
    elif option == '6':
        db.store_in_db(math_instance)
    
    elif option == '7':
        print("Saliendo del programa...")
        break
    
    else:
        print("Opción no válida, por favor intenta de nuevo")
