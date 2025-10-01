from fastapi import HTTPException, status

# 使用者相關錯誤
class UserAlreadyExists(HTTPException):
    def __init__(self, detail: str = "使用者已存在"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class EmailAlreadyExists(HTTPException):
    def __init__(self, detail: str = "電子郵件已存在"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UserNotFound(HTTPException):
    def __init__(self, detail: str = "使用者不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class InvalidPassword(HTTPException):
    def __init__(self, detail: str = "密碼錯誤"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

# Token 相關錯誤
class InvalidToken(HTTPException):
    def __init__(self, detail: str = "Token 無效"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

# 商品相關錯誤
class ProductNotFound(HTTPException):
    def __init__(self, detail: str = "商品不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class OutOfStock(HTTPException):
    def __init__(self, detail: str = "庫存不足"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

# 訂單相關錯誤
class OrderNotFound(HTTPException):
    def __init__(self, detail: str = "訂單不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)