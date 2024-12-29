from core.models import WorkflowTransition


def can_transition(current_status, next_status):
    return WorkflowTransition.objects.filter(
        from_status=current_status, 
        to_status=next_status
    ).exists()