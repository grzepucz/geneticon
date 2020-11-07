import json
import random
import string

from django.http import HttpResponse
from geneticon.models import OptimizationMethod, Population, Selection, Hybridization, Mutation, Inversion, Life, \
    Subject, Chromosome, Gene
from .functions import BohachevskyFormula, BoothFormula


def create_gene(chromosome):
    for i in range(chromosome.size):
        gene = Gene(allel=round(random.random()), locus=i, chromosome=chromosome)
        gene.save()


def create_chromosome(subject):
    chromosome = Chromosome(size=25, subject=subject)
    chromosome.save()
    create_gene(chromosome)


def create_subjects(population):
    for i in range(int(population.size)):
        subject = Subject(population=population)
        subject.name = ''.join(random.choice(string.ascii_lowercase) for j in range(10))
        subject.save()
        create_chromosome(subject)


def save_form_data(form):
    selection = Selection(
        type=form.data['selection_type'],
        settings=form.data['selection_settings']
    )
    selection.save()

    mutation = Mutation(
        type=form.data['mutation_type'],
        probability=form.data['mutation_probability']
    )
    mutation.save()

    hybridization = Hybridization(
        type=form.data['hybridization_type'],
        probability=form.data['hybridization_probability']
    )
    hybridization.save()

    inversion = Inversion(probability=form.data['inversion_probability'])
    inversion.save()

    population = Population(
        name=form.data['population_name'],
        size=form.data['population_size']
    )
    population.save()

    create_subjects(population)

    life = Life(population=population,
                epochs=form.data['epochs_number'],
                selection=selection,
                hybridization=hybridization,
                mutation=mutation,
                inversion=inversion,
                elite_strategy=form.data['elite_strategy'],
                function=OptimizationMethod.objects.get(id=form.data['optimization_function']))
    life.save()

    return life.id


def create_sample_configuration():
    bohachevsky = OptimizationMethod(
        id=1,
        domain_minimum=-100,
        domain_maximum=100,
        body='(x1^2) + (2 * (x2^2)) - (0.3 * cos(3 * pi * x1)) - (0.4 * cos(4 * pi * x2))',
        name='Bohachevsky')
    bohachevsky.formula = BohachevskyFormula
    bohachevsky.save()

    booth = OptimizationMethod(
        id=2,
        body='(x1 + 2 * x2 - 7)^2 + (2 * x1 + x2 - 5)^2',
        domain_minimum=-10,
        domain_maximum=10,
        name='Booth')
    booth.formula = BoothFormula
    booth.save()

    selection = Selection(id=1, type='TOURNAMENT', settings=json.JSONEncoder().encode({'group_size': 4}))
    selection.save()

    mutation = Mutation(id=1, type='EDGE', probability=0.1)
    mutation.save()

    hybridization = Hybridization(id=1, type='SINGLE', probability=0.8)
    hybridization.save()

    inversion = Inversion(id=1, probability=0.1)
    inversion.save()

    population = Population(id=1, name='Test', size=12)
    population.save()

    create_subjects(population)

    life = Life(population=population,
                generations=20,
                selection=selection,
                hybridization=hybridization,
                mutation=mutation,
                inversion=inversion,
                elite_strategy=0.3,
                function=booth)
    life.save()


def sample_configuration(request):
    create_sample_configuration()
    return HttpResponse(200)
