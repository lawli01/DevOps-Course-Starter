from todo_app.data.item import Item, ItemStatus
from todo_app.data.itemsViewModel import ItemsViewModel


items = [
    Item(id="1", title="TODO", status=ItemStatus.NOT_STARTED),
    Item(id="2",title="DOING", status=ItemStatus.IN_PROGRESS),
    Item(id="3",title="DONE", status=ItemStatus.COMPLETE),
]

empty_view_model = ItemsViewModel(items=[])
view_model = ItemsViewModel(items=items)

class TestItemsViewModel:
    @staticmethod
    def test_can_get_todo_items():
        # Act
        to_do_items = view_model.to_do_items

        # Assert
        assert len(to_do_items) is 1
        assert to_do_items[0].title is "TODO"
        assert to_do_items[0].status is ItemStatus.NOT_STARTED

    @staticmethod
    def test_returns_empty_if_no_to_dos():
        # Act
        to_do_items = empty_view_model.to_do_items

        # Assert
        assert len(to_do_items) is 0

    @staticmethod
    def test_can_get_doing_items():
        # Act
        doing_items = view_model.doing_items

        # Assert
        assert len(doing_items) is 1
        assert doing_items[0].title is "DOING"
        assert doing_items[0].status is ItemStatus.IN_PROGRESS

    @staticmethod
    def test_returns_empty_if_no_doing_items():
        # Act
        doing_items = empty_view_model.doing_items

        # Assert
        assert len(doing_items) is 0

    @staticmethod
    def test_can_get_done_items():
        # Act
        done_items = view_model.done_items

        # Assert
        assert len(done_items) is 1
        assert done_items[0].title is "DONE"
        assert done_items[0].status is ItemStatus.COMPLETE

    @staticmethod
    def test_returns_empty_if_no_done_items():
        # Act
        done_items = empty_view_model.done_items

        # Assert
        assert len(done_items) is 0