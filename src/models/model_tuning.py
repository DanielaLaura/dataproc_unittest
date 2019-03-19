
import plot_precision_recall
#import first the precision recall data
pr_data = plot_precision_recall(
    test_y, probs, title='Precision-Recall Curve for Random Forest')
recall_attained = 0.75
recall_above = pr_data.loc[pr_data['recall'] >= recall_attained].copy()
recall_above.sort_values('precision', ascending=False, inplace=True)
precision_attained = recall_above.iloc[0, 0]
threshold_required = recall_above.iloc[0, -1]
#pr_data = plot_precision_recall(test_y, probs, title='Precision-Recall Curve for Tuned Random Forest',
                               # threshold_selected=threshold_required)
print(
    f'At a threshold of {round(threshold_required, 4)} the recall is {100 * recall_attained:.2f}% and the precision is {round(100 * precision_attained, 4)}%')





