import math
import random
import string

from geneticon.models import Subject, Chromosome, Gene
from .mutation import mutate
from .inversion import inverse


def create_subjects(representation):
    if representation == 'BINARY':
        return create_subjects_binary
    if representation == 'REAL':
        return create_subjects_real


def create_subjects_binary(reflect_offspring, epoch):
    offspring = []
    for parent in reflect_offspring:
        clone = Subject(name=parent.name, population=parent.population, epoch=epoch)
        clone.save()
        for parent_chromosome in Chromosome.objects.filter(subject=parent):
            chromosome = Chromosome(size=parent_chromosome.size, subject=clone)
            chromosome.save()
            for parent_gene in Gene.objects.filter(chromosome=parent_chromosome):
                gene = Gene(allel=parent_gene.allel, locus=parent_gene.locus, chromosome=chromosome)
                gene.save()
        offspring.append(clone)
    return offspring


def create_subjects_real(reflect_offspring, epoch):
    offspring = []
    for parent in reflect_offspring:
        clone = Subject(name=parent.name, population=parent.population, epoch=epoch)
        clone.save()
        for parent_chromosome in Chromosome.objects.filter(subject=parent):
            chromosome = Chromosome(size=parent_chromosome.size, subject=clone, real_value=parent_chromosome.real_value)
            chromosome.save()
        offspring.append(clone)
    return offspring


def create_offspring(life_model, parents, epoch, previous_population_length):
    offspring = []
    create_subjects_method = create_subjects(life_model.representation)

    if len(parents) == 1:
        return create_subjects_method(parents[0:1], epoch)

    if 0 < life_model.elite_strategy * previous_population_length <= len(parents):
        offspring = create_subjects_method(
            parents[:math.ceil(life_model.elite_strategy * previous_population_length)],
            epoch
        )

    # Subjects kept by elite strategy are not included in operations below
    for index in range(len(offspring)):
        subject = offspring[index]
        mutate(subject, life_model.mutation.type, life_model.mutation.probability, life_model.function)
        inverse(subject, life_model.inversion.probability)

    for index in range(len(parents)):
        subject = [parents[index]]
        if random.random() <= life_model.hybridization.probability:
            subject = crossover(parents, index, life_model, epoch)
        subject = [mutate(item, life_model.mutation.type, life_model.mutation.probability, life_model.function) for item
                   in subject]
        subject = [inverse(item, life_model.inversion.probability) for item in subject]
        for item in subject:
            offspring.append(item)

    return offspring


def get_non_self_random_index(range_end, index):
    rand = random.randint(0, range_end - 1)
    while rand == index:
        rand = random.randint(0, range_end - 1)
    return rand


def create_sibilings(life_model, epoch):
    boy = Subject()
    boy.name = ''.join(random.choice(string.ascii_lowercase) for j in range(10))
    boy.epoch = epoch
    boy.population = life_model.population
    boy.save()

    girl = Subject()
    girl.name = ''.join(random.choice(string.ascii_lowercase) for j in range(10))
    girl.epoch = epoch
    girl.population = life_model.population
    girl.save()

    return [boy, girl]


def create_chromosomes(size, children):
    chromosome_boy = Chromosome(size=size, subject=children[0])
    chromosome_boy.save()

    chromosome_girl = Chromosome(size=size, subject=children[1])
    chromosome_girl.save()

    return [chromosome_boy, chromosome_girl]


def single_crossover(chromosomes, partner_chromosomes, children):
    for chromosome_index in range(len(chromosomes)):
        children_chromosomes = create_chromosomes(chromosomes[chromosome_index].size, children)
        genes_x = Gene.objects.filter(chromosome=chromosomes[chromosome_index]).order_by('locus')
        genes_y = Gene.objects.filter(
            chromosome=partner_chromosomes[chromosome_index]).order_by('locus')
        pivot = random.randint(1, chromosomes[chromosome_index].size)

        for gene_index in range(len(genes_x)):
            genes = [Gene() for chromosome in children_chromosomes]
            for index in range(len(genes)):
                if gene_index < pivot:
                    genes[index].allel = genes_x[gene_index].allel if index % 2 == 0 else genes_y[gene_index].allel
                    genes[index].locus = genes_x[gene_index].locus if index % 2 == 0 else genes_y[gene_index].locus
                else:
                    genes[index].allel = genes_y[gene_index].allel if index % 2 == 0 else genes_x[gene_index].allel
                    genes[index].locus = genes_y[gene_index].locus if index % 2 == 0 else genes_x[gene_index].locus
                genes[index].chromosome = children_chromosomes[index]
                genes[index].save()
    return children


def double_crossover(chromosomes, partner_chromosomes, children):
    for chromosome_index in range(len(chromosomes)):
        children_chromosomes = create_chromosomes(chromosomes[chromosome_index].size, children)
        genes_x = Gene.objects.filter(chromosome=chromosomes[chromosome_index]).order_by('locus')
        genes_y = Gene.objects.filter(
            chromosome=partner_chromosomes[chromosome_index]).order_by('locus')
        pivot = sorted(random.sample(range(1, chromosomes[chromosome_index].size), 2), key=lambda x: x)
        for gene_index in range(len(genes_x)):
            genes = [Gene() for chromosome in children_chromosomes]
            for index in range(len(genes)):
                if min(pivot) <= gene_index < max(pivot):
                    genes[index].allel = genes_x[gene_index].allel if index % 2 == 0 else genes_y[gene_index].allel
                    genes[index].locus = genes_x[gene_index].locus if index % 2 == 0 else genes_y[gene_index].locus
                else:
                    genes[index].allel = genes_y[gene_index].allel if index % 2 == 0 else genes_x[gene_index].allel
                    genes[index].locus = genes_y[gene_index].locus if index % 2 == 0 else genes_x[gene_index].locus
                genes[index].chromosome = children_chromosomes[index]
                genes[index].save()
    return children


def triple_crossover(chromosomes, partner_chromosomes, children):
    for chromosome_index in range(len(chromosomes)):
        children_chromosomes = create_chromosomes(chromosomes[chromosome_index].size, children)
        genes_x = Gene.objects.filter(chromosome=chromosomes[chromosome_index]).order_by('locus')
        genes_y = Gene.objects.filter(
            chromosome=partner_chromosomes[chromosome_index]).order_by('locus')
        pivot = sorted(random.sample(range(1, chromosomes[chromosome_index].size), 3), key=lambda x: x)
        for gene_index in range(len(genes_x)):
            genes = [Gene() for chromosome in children_chromosomes]
            for index in range(len(genes)):
                if (gene_index < pivot[0]) or (pivot[1] < gene_index < pivot[2]):
                    genes[index].allel = genes_x[gene_index].allel if index % 2 == 0 else genes_y[gene_index].allel
                    genes[index].locus = genes_x[gene_index].locus if index % 2 == 0 else genes_y[gene_index].locus
                else:
                    genes[index].allel = genes_y[gene_index].allel if index % 2 == 0 else genes_x[gene_index].allel
                    genes[index].locus = genes_y[gene_index].locus if index % 2 == 0 else genes_x[gene_index].locus
                genes[index].chromosome = children_chromosomes[index]
                genes[index].save()
    return children


def homogeneous_crossover(chromosomes, partner_chromosomes, children):
    for chromosome_index in range(len(chromosomes)):
        children_chromosomes = create_chromosomes(chromosomes[chromosome_index].size, children)
        genes_x = Gene.objects.filter(chromosome=chromosomes[chromosome_index]).order_by('locus')
        genes_y = Gene.objects.filter(
            chromosome=partner_chromosomes[chromosome_index]).order_by('locus')

        for gene_index in range(len(genes_x)):
            genes = [Gene() for chromosome in children_chromosomes]
            for index in range(len(genes)):
                if gene_index % 2 == 0:
                    genes[index].allel = genes_x[gene_index].allel if index % 2 == 0 else genes_y[gene_index].allel
                    genes[index].locus = genes_x[gene_index].locus if index % 2 == 0 else genes_y[gene_index].locus
                else:
                    genes[index].allel = genes_y[gene_index].allel if index % 2 == 0 else genes_x[gene_index].allel
                    genes[index].locus = genes_y[gene_index].locus if index % 2 == 0 else genes_x[gene_index].locus
                genes[index].chromosome = children_chromosomes[index]
                genes[index].save()
    return children


def arithmetic_crossover(chromosomes, partner_chromosomes, children):
    factor = random.random()

    for chromosome_index in range(len(chromosomes)):
        [boy_chromosome, girl_chromosome] = create_chromosomes(chromosomes[chromosome_index].size, children)
        boy_chromosome.real_value = factor * chromosomes[chromosome_index].real_value + (1 - factor) * \
                                    partner_chromosomes[chromosome_index].real_value
        girl_chromosome.real_value = (1 - factor) * chromosomes[chromosome_index].real_value + factor * \
                                     partner_chromosomes[chromosome_index].real_value

        boy_chromosome.save()
        girl_chromosome.save()

    return children


def heuristic_crossover(chromosomes, partner_chromosomes, life_model, epoch):
    child = Subject(
        name=''.join(random.choice(string.ascii_lowercase) for j in range(10)),
        population=life_model.population,
        epoch=epoch)
    child.save()
    factor = random.random()

    for index in range(len(chromosomes)):
        chromosome = Chromosome(subject=child)
        chromosome.real_value = factor * abs(
            partner_chromosomes[index].real_value - chromosomes[index].real_value) + min(
            partner_chromosomes[index].real_value,
            chromosomes[index].real_value)
        chromosome.save()

    return [child]


def crossover(parents, index, life_model, epoch):
    partner_index = get_non_self_random_index(len(parents), index)
    partner = parents[partner_index]
    chromosomes = Chromosome.objects.filter(subject=parents[index])
    partner_chromosomes = Chromosome.objects.filter(subject=partner)

    if life_model.hybridization.type == 'SINGLE':
        return single_crossover(chromosomes, partner_chromosomes, create_sibilings(life_model, epoch))
    if life_model.hybridization.type == 'DOUBLE':
        return double_crossover(chromosomes, partner_chromosomes, create_sibilings(life_model, epoch))
    if life_model.hybridization.type == 'TRIPLE':
        return triple_crossover(chromosomes, partner_chromosomes, create_sibilings(life_model, epoch))
    if life_model.hybridization.type == 'HOMO':
        return homogeneous_crossover(chromosomes, partner_chromosomes, create_sibilings(life_model, epoch))
    if life_model.hybridization.type == 'ARITHMETIC':
        return arithmetic_crossover(chromosomes, partner_chromosomes, create_sibilings(life_model, epoch))
    if life_model.hybridization.type == 'HEURISTIC':
        return heuristic_crossover(chromosomes, partner_chromosomes, life_model, epoch)

    return False
