from ankivalenz import BasicCard, NodeParser
from ankivalenz.types import ClozeCard, Node, Delimeter, BasicCard

class TestQuestionAnswer:
    def setup_method(self):
        nodes = [
            ("Question", Delimeter("?::"), "Answer")
        ]

        self.cards = NodeParser().parse(nodes)

    def test_finds_one_card(self):
        assert 1 == len(self.cards), self.cards

    def test_type(self):
        assert isinstance(self.cards[0], BasicCard)

    def test_question(self):
        assert "Question" == self.cards[0].question

    def test_answer(self):
        assert "Answer" == self.cards[0].answer

class TestAnswerQuestion:
    def setup_method(self):
        nodes = [
            ("Answer", Delimeter("::?"), "Question")
        ]

        self.cards = NodeParser().parse(nodes)

    def test_finds_one_card(self):
        assert 1 == len(self.cards)

    def test_type(self):
        assert isinstance(self.cards[0], BasicCard)

    def test_question(self):
        assert "Question" == self.cards[0].question

    def test_answer(self):
        assert "Answer" == self.cards[0].answer

class TestTwoWay:
    def setup_method(self):
        nodes = [
            ("Question", Delimeter("::"), "Answer")
        ]

        self.cards = NodeParser().parse(nodes)

    def test_finds_one_card(self):
        assert 1 == len(self.cards)

    def test_type(self):
        assert isinstance(self.cards[0], BasicCard)

    def test_question(self):
        assert "Question" == self.cards[0].question

    def test_answer(self):
        assert "Answer" == self.cards[0].answer

    def test_reverse(self):
        assert True == self.cards[0].reverse

class TestCloze:
    def setup_method(self):
        nodes = [
            ("A {{c1::Cloze}} Deletion")
        ]

        self.cards = NodeParser().parse(nodes)

    def test_finds_one_card(self):
        assert 1 == len(self.cards)

    def test_type(self):
        assert isinstance(self.cards[0], ClozeCard)

    def test_question(self):
        assert "A {{c1::Cloze}} Deletion" == self.cards[0].question

class TestNestedSingleLevel:
    def setup_method(self):
        nodes = [
            ("Header", [
                ("Question 1", Delimeter("?::"), "Answer 1")
            ])
        ]

        self.cards = NodeParser().parse(nodes)
    
    def test_finds_one_card(self):
        assert 1 == len(self.cards)
    
    def test_path(self):
        assert ["Header"] == self.cards[0].path
    
class TestNestedMultipleLevels:
    def setup_method(self):
        nodes = [
            ("Header 1", [
                ("Header 2", [
                    ("Question 1", Delimeter("?::"), "Answer 1")
                ])
            ])
        ]

        self.cards = NodeParser().parse(nodes)
    
    def test_finds_one_card(self):
        assert 1 == len(self.cards)
    
    def test_path(self):
        assert ["Header 1", "Header 2"] == self.cards[0].path

class TestMultipleNestedLists:
    def setup_method(self):
        nodes = [
            ("List 1", [
                ("Question 1", Delimeter("?::"), "Answer 1")
            ]),
            ("List 2", [
                ("Question 2", Delimeter("?::"), "Answer 2")
            ])
        ]

        self.cards = NodeParser().parse(nodes)
    
    def test_finds_two_cards(self):
        assert 2 == len(self.cards)
    
    def test_path(self):
        assert ["List 1"] == self.cards[0].path
        assert ["List 2"] == self.cards[1].path

class TestNestedStandaloneQuestion:
    def setup_method(self):
        nodes = [
            ("Header 1", [
                ("Answer", [
                    (Delimeter("::?"), "Question")
                ])
            ])
        ]

        self.cards = NodeParser().parse(nodes)

    def test_finds_one_card(self):
        assert 1 == len(self.cards)
    
    def test_question(self):
        assert "Question" == self.cards[0].question
    
    def test_answer(self):
        assert "Answer" == self.cards[0].answer
    
    def test_path(self):
        assert ["Header 1"] == self.cards[0].path


class TestNestedStandaloneAnswer:
    def setup_method(self):
        nodes = [
            ("Header 1", [
                ("Question", [
                    (Delimeter("?::"), "Answer")
                ])
            ])
        ]

        self.cards = NodeParser().parse(nodes)

    def test_finds_one_card(self):
        assert 1 == len(self.cards)
    
    def test_question(self):
        assert "Question" == self.cards[0].question
    
    def test_answer(self):
        assert "Answer" == self.cards[0].answer
    
    def test_path(self):
        assert ["Header 1"] == self.cards[0].path

class TestNestedStandaloneTwoWay:
    def setup_method(self):
        nodes = [
            ("Header 1", [
                ("Side 1", [
                    (Delimeter("::"), "Side 2")
                ])
            ])
        ]

        self.cards = NodeParser().parse(nodes)

    def test_finds_one_card(self):
        assert 1 == len(self.cards)
    
    def test_question(self):
        assert "Side 1" == self.cards[0].question
    
    def test_answer(self):
        assert "Side 2" == self.cards[0].answer
    
    def test_reverse(self):
        assert True == self.cards[0].reverse
    
    def test_path(self):
        assert ["Header 1"] == self.cards[0].path
