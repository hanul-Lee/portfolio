export const approvalStatus = {
  draft: '임시저장',
  pending: '승인대기',
  approved: '승인완료',
  rejected: '반려',
};
export const currentApprover = (doc) =>
  doc.approverIds[doc.decisions.filter((d) => d.action === 'approve').length];
export function approvalBuckets(docs, userId) {
  return [
    docs.filter((d) => d.ownerId === userId),
    docs.filter((d) => d.status === 'pending' && currentApprover(d) === userId),
    docs.filter((d) => d.ownerId === userId && d.status === 'rejected'),
  ];
}
