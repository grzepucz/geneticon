from django import forms
from django.forms import NumberInput

from .models import OptimizationMethod, Selection, Hybridization, Mutation, Life
from django.core.validators import MaxValueValidator, MinValueValidator


class EpochForm(forms.Form):
    epoch_number = forms.ChoiceField(choices=[], widget=forms.Select, required=True)

    def __init__(self, epoch_numbers_, *args, **kwargs):
        super(EpochForm, self).__init__(*args, **kwargs)
        self.fields['epoch_number'].choices = epoch_numbers_


class PopulationForm(forms.Form):
    population_size = forms.IntegerField(label='Population size', required=True,
                                         widget=NumberInput(attrs={'step': "1"}))
    population_name = forms.CharField(label='Population name', required=True)

    representation = forms.ChoiceField(label='Chromosome representation', required=True, widget=forms.Select,
                                       choices=Life.representation_choices)

    problem = forms.ChoiceField(label='Optimization problem', required=True, widget=forms.Select,
                                choices=Life.problem_choices)
    methods = [[model.id, model.name] for model in OptimizationMethod.objects.all()]
    optimization_function = forms.ChoiceField(
        label='Optimize function',
        required=True,
        widget=forms.Select,
        choices=methods
    )
    epochs_number = forms.IntegerField(label='Epochs number',
                                       widget=NumberInput(attrs={'step': "1"}))
    precision = forms.IntegerField(label='Precision of result in digits after comma.',
                                   widget=NumberInput(attrs={'step': "1"}))
    selection_type = forms.ChoiceField(
        label='Selection type',
        required=True,
        widget=forms.Select,
        choices=Selection.choices)
    selection_settings = forms.CharField(label='Selection settings in JSON format. Use schema from description',
                                         initial='{}')

    hybridization_type = forms.ChoiceField(
        label='Hybridization type',
        required=True,
        widget=forms.Select,
        choices=Hybridization.choices)
    hybridization_probability = forms.FloatField(
        label='Hybridization probability in range 0 - 1',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        widget=NumberInput(attrs={'step': "0.01"})
    )

    mutation_type = forms.ChoiceField(
        label='Mutation type',
        required=True,
        widget=forms.Select,
        choices=Mutation.choices)
    mutation_probability = forms.FloatField(
        label='Mutation probability in range 0 - 1',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        widget=NumberInput(attrs={'step': "0.01"}))

    inversion_probability = forms.FloatField(
        label='Inversion probability in range 0 - 1',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        widget=NumberInput(attrs={'step': "0.01"}))

    elite_strategy = forms.FloatField(
        label='Elite strategy as percent in range 0-1',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        widget=NumberInput(attrs={'step': "0.01"}))
