import abc
import pandas as pd

class Base(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def login(self, user_id: str, user_password: str):
        pass

    @abc.abstractmethod
    def get_borrow_list(self) -> pd.DataFrame:
       pass

    @abc.abstractmethod
    def push_extension_button(self, book_id: str) -> None:
       pass
