from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модель данных
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# Хранилище данных
items: List[Item] = []

# =====================
# HTML-интерфейс
# =====================
@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple FastAPI Site</title>
    </head>
    <body>
        <h1>Simple FastAPI Item Manager</h1>

        <h2>Add Item</h2>
        <input type="text" id="name" placeholder="Name">
        <input type="number" id="price" placeholder="Price">
        <label>Offer: <input type="checkbox" id="is_offer"></label>
        <button onclick="addItem()">Add</button>

        <h2>Items</h2>
        <ul id="itemList"></ul>

        <script>
            async function fetchItems() {
                const response = await fetch('/items/');
                const data = await response.json();
                const list = document.getElementById('itemList');
                list.innerHTML = '';
                data.forEach((item, index) => {
                    const li = document.createElement('li');
                    li.textContent = `${item.name} - $${item.price} - Offer: ${item.is_offer}`;
                    const delBtn = document.createElement('button');
                    delBtn.textContent = 'Delete';
                    delBtn.onclick = () => deleteItem(index);
                    li.appendChild(delBtn);
                    list.appendChild(li);
                });
            }

            async function addItem() {
                const name = document.getElementById('name').value;
                const price = parseFloat(document.getElementById('price').value);
                const is_offer = document.getElementById('is_offer').checked;
                await fetch('/items/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, price, is_offer})
                });
                document.getElementById('name').value = '';
                document.getElementById('price').value = '';
                document.getElementById('is_offer').checked = false;
                fetchItems();
            }

            async function deleteItem(index) {
                await fetch(`/items/${index}`, { method: 'DELETE' });
                fetchItems();
            }

            // Загружаем список при старте
            fetchItems();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# =====================
# API Методы
# =====================
@app.post("/items/")
def create_item(item: Item):
    items.append(item)
    return {"message": "Item added", "item": item}

@app.get("/items/")
def get_items():
    return items

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if 0 <= item_id < len(items):
        removed_item = items.pop(item_id)
        return {"message": "Item deleted", "item": removed_item}
    return {"error": "Item not found"}
