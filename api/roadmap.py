from models import RoadmapNode

class RoadmapEngine:
    def construct_tree(self, tasks: list) -> list:
        nodes = []
        for i, task in enumerate(tasks):
            nodes.append(RoadmapNode(
                title=task,
                is_locked=True if i > 0 else False,
                node_type="start" if i == 0 else "breadcrumb"
            ))
        return nodes