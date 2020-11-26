from ArraySequence import ArraySeq as Seq



def merge(lres, rres, left_length):
    (leftmost_left_unmactched_from_start1, rightmost_right_unmactched_from_start1, left_unmatched1, right_unmachted1, max_dist1) = lres
    (leftmost_left_unmactched_from_start2, rightmost_right_unmactched_from_start2, left_unmatched2, right_unmachted2, max_dist2) = rres

    final_maxdist = max(max_dist1, max_dist2)
    if leftmost_left_unmactched_from_start1 != -1 and rightmost_right_unmactched_from_start2 != -1:
        final_maxdist = max(final_maxdist, rightmost_right_unmactched_from_start2 + (left_length - leftmost_left_unmactched_from_start1) - 1)

    if left_unmatched1 == right_unmachted2:
        if leftmost_left_unmactched_from_start2 != -1:
            return (leftmost_left_unmactched_from_start2 + left_length, rightmost_right_unmactched_from_start1, left_unmatched2, right_unmachted1, final_maxdist)
        else:
            return (leftmost_left_unmactched_from_start2, rightmost_right_unmactched_from_start1, left_unmatched2, right_unmachted1, final_maxdist)

    elif left_unmatched1 > right_unmachted2:
        return (leftmost_left_unmactched_from_start1, rightmost_right_unmactched_from_start1, left_unmatched1 - right_unmachted2 + left_unmatched2, right_unmachted1, final_maxdist)
        
    else: # left_unmatched1 < right_unmachted2
        if leftmost_left_unmactched_from_start2 != -1:
            return (leftmost_left_unmactched_from_start2 + left_length, rightmost_right_unmactched_from_start2 + left_length, left_unmatched2, right_unmachted2 - left_unmatched1 + right_unmachted1, final_maxdist)
        else:
            return (leftmost_left_unmactched_from_start2, rightmost_right_unmactched_from_start2 + left_length, left_unmatched2, right_unmachted2 - left_unmatched1 + right_unmachted1, final_maxdist)


# paren is string seq
def compute(paren):
    if Seq.length(paren) == 0:
        return None
    elif Seq.length(paren) == 1:
        p = Seq.nth(paren, 0)
        if p == "(":
            return (0, -1, 1, 0, 0)
        elif p == ")":
            return (-1, 0, 0, 1, 0)
    else:
        left, right = Seq.splitMid(paren)
        lres, rres = compute(left), compute(right)
        return merge(lres, rres, Seq.length(left))


def MPD(paren):
    if Seq.length(paren) <= 1:
        return 0
    else:
        res = compute(paren)
        return res[4] if (res[0] == res[1] == -1) else 0
