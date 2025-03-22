from ninja import Schema


class StudyPlannerIn(Schema):
    syllabus: list[str]
    study_hours: int
