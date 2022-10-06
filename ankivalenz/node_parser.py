from typing import List
from .types import Node, Delimeter, BasicCard, Card, ClozeCard


class NodeParser:
    def parse(
        self, nodes: Node, cards: List[Card] = None, path: List[str] = None
    ) -> List[Card]:
        if cards is None:
            cards = []

        if path is None:
            path = []

        match nodes:
            case list(l):
                for node in l:
                    self.parse(node, cards, path.copy())
            case (str(header), list(l)):
                path.append(header)
                return self.parse(l, cards, path.copy())
            case str(question):
                return cards.append(ClozeCard(question, path.copy()))
            case (Delimeter("::"), str(answer)):
                return cards.append(
                    BasicCard(path[-1], answer, path[:-1], reverse=True)
                )
            case (Delimeter("?::"), str(answer)):
                return cards.append(BasicCard(path[-1], answer, path[:-1]))
            case (Delimeter("::?"), str(question)):
                return cards.append(BasicCard(question, path[-1], path[:-1]))
            case (str(question), Delimeter("?::"), str(answer)):
                return cards.extend([BasicCard(question, answer, path.copy())])
            case (str(answer), Delimeter("::?"), str(question)):
                return cards.extend([BasicCard(question, answer, path.copy())])
            case (str(question), Delimeter("::"), str(answer)):
                return cards.extend(
                    [BasicCard(question, answer, path.copy(), reverse=True)]
                )

        return cards
